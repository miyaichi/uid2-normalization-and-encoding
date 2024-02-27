import base64
import boto3
import cgi
import datetime
import hashlib
import io
import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')


# Store uploaded files in S3
def upload_file_to_s3(event, context):
    logger.info("New file uploaded.")

    # Generate file name in YYYYMMDD-HHMMSS.csv format using the current time.
    key = datetime.datetime.now(
        datetime.timezone(datetime.timedelta(hours=9),
                          'JST')).strftime("%Y%m%d-%H%M%S.csv")

    # Parse multi-part data
    _, c_data = cgi.parse_header(event['headers']['content-type'])
    c_data['boundary'] = bytes(c_data['boundary'], 'utf8')
    form_data = cgi.parse_multipart(io.BytesIO(bytes(event['body'], 'utf8')),
                                    c_data)

    # Store in S3
    s3.put_object(Bucket=os.environ['source_bucket'],
                  Key=key,
                  Body=form_data['file'][0])

    # Create presigned URL of normalized and encoding file
    location = s3.generate_presigned_url(ClientMethod='get_object',
                                         Params={
                                             'Bucket':
                                             os.environ['destination_bucket'],
                                             'Key':
                                             key
                                         },
                                         ExpiresIn=3600,
                                         HttpMethod='GET')

    return {
        "statusCode": 200,
        "body": json.dumps({
            "uploaded": "true",
            "location": location
        })
    }


# Normalize and encoding email addresses in S3 bucket files
def normalization_and_encoding(event, context):
    logger.info("New files uploaded to the source bucket.")

    key = event['Records'][0]['s3']['object']['key']
    source_bucket = event['Records'][0]['s3']['bucket']['name']

    logger.info("source: {}, key: {}".format(source_bucket, key))

    buffer = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")
    source = s3.get_object(Bucket=source_bucket, Key=key)
    for line in source['Body']._raw_stream:
        data_str = line.decode('utf-8').rstrip()
        if len(data_str):
            encoded = ''
            if is_email(data_str):
                encoded = base64_encode(
                    hash_sha256(normalize_email_string(data_str)))
                buffer.write("{}\n".format(encoded))

    # Write to destination bucket
    buffer.seek(0)
    s3.put_object(Bucket=os.environ['destination_bucket'],
                  Key=key,
                  Body=buffer.read())

    # Delete source file
    s3.delete_object(Bucket=source_bucket, Key=key)


# Determine if the string is a email address
def is_email(data):
    if data.count('@') != 1:
        return False
    _, domain = data.split('@')
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
