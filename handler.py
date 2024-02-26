import base64
import boto3
import hashlib
import io
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')


# Normalize and encoding email addresses in S3 bucket files
def normalization_and_encoding(event, context):
    logger.info("New files uploaded to the source bucket.")

    key = event['Records'][0]['s3']['object']['key']
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    destination_bucket = os.environ['destination_bucket']

    logger.info("source: {}, key: {}".format(source_bucket, key))

    buffer = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")
    source = s3.get_object(Bucket=source_bucket, Key=key)
    for line in source['Body']._raw_stream:
        data_str = line.decode('utf-8').rstrip()
        if len(data_str):
            email = encoded = ''
            if is_email(data_str):
                email = normalize_email_string(data_str)
                encoded = base64_encode(hash_sha256(email))

            buffer.write("{},{},{}\n".format(data_str, email, encoded))

    # Write to destination bucket
    buffer.seek(0)
    s3.put_object(Bucket=destination_bucket, Key=key, Body=buffer.read())


# Determine if the string is a email address
def is_email(data):
    if data.count('@') != 1:
        return False
    local, domain = data.split('@')
    if domain.count('.') != 1:
        return False
    return True


# Normalise email string
def normalize_email_string(email):
    # Remove leading and trailing spaces.
    email = email.strip()
    # Convert to lowercase
    email = email.lower()
    # In gmail.com addresses only
    if email.endswith('@gmail.com'):
        local, domain = email.split('@')
        # Remove all dots in the local part
        local = local.replace('.', '')
        # Remove everything after the first plus sign
        local = local.split('+')[0]
        email = local + '@' + domain
    return email


# Base64 encode
def base64_encode(b):
    return base64.b64encode(b).decode()


# Hash with SHA256
def hash_sha256(data):
    return hashlib.sha256(data.encode()).digest()
