# -*- coding: utf-8 -*-
import base64
import boto3
import cgi
import datetime
import hashlib
import io
import jinja2
import json
import logging
import os
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
environment = jinja2.Environment(loader=jinja2.FileSystemLoader(
    searchpath='./templates'))


# Store uploaded files in S3.
def upload_file_to_s3(event, context):
    logger.info("New file uploaded.")
    logger.info("Received event {}".format(json.dumps(event)))

    if event['httpMethod'] == 'GET':
        # Returns a form for uploading file.
        template = environment.get_template('upload.tpl')
        return {
            "statusCode":
            200,
            "headers": {
                'Content-Type': 'text/html'
            },
            "body":
            template.render({
                "domain": event['requestContext']['domainName'],
                "path": event['requestContext']['resourcePath'],
                "stage": event['requestContext']['stage']
            })
        }

    if event['httpMethod'] == 'POST':
        # Generate file name in YYYYMMDD-HHMMSS.csv format using the current time.
        key = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=9),
                              'JST')).strftime("%Y%m%d-%H%M%S.csv")

        # Parse multi-part data.
        _, c_data = cgi.parse_header(event['headers']['content-type'])
        c_data['boundary'] = bytes(c_data['boundary'], 'utf8')
        form_data = cgi.parse_multipart(
            io.BytesIO(bytes(event['body'], 'utf8')), c_data)

        # Store in S3.
        s3.put_object(Bucket=os.environ['source_bucket'],
                      Key=key,
                      Body=form_data['file'][0])

        # Create presigned URL of normalized and encoding file.
        location = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': os.environ['destination_bucket'],
                'Key': key
            },
            ExpiresIn=os.environ['expires_in'],
            HttpMethod='GET')

        # Returns a link to download a file.
        template = environment.get_template('download.tpl')
        return {
            "statusCode": 200,
            "headers": {
                'Content-Type': 'text/html'
            },
            "body": template.render({
                "key": key,
                "location": location
            })
        }


# Clean up buckets
def clean_up_buckets(event, context):
    logger.info("Clean up source and destination bucket.")

    # Expires_in seconds before current time.
    date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
        seconds=os.environ['expires_in'])

    # Scan buckets and delete old objects.
    buckets = [os.environ['source_bucket'], os.environ['destination_bucket']]
    for bucket in buckets:
        response = s3.list_objects_v2(Bucket=bucket)
        if 'Contents' in response:
            for obj in response['Contents']:
                last_modified = obj['LastModified']
                key = obj['Key']
                if last_modified < date:
                    # Delete expired object.
                    s3.delete_object(Bucket=bucket, Key=key)
                logger.info(
                    "Deleted Key {} in Bucket {} (last_modified: {}).".format(
                        key, bucket, last_modified))

    return {"statusCode": 200}


# Normalize and encoding email addresses in S3 bucket files.
def normalization_and_encoding(event, context):
    logger.info("New files uploaded to the source bucket.")

    key = event['Records'][0]['s3']['object']['key']
    source_bucket = event['Records'][0]['s3']['bucket']['name']

    logger.info("source: {}, key: {}".format(source_bucket, key))

    source = s3.get_object(Bucket=source_bucket, Key=key)
    encoded_list = []
    for line in source['Body']._raw_stream:
        data_str = line.decode('utf-8').rstrip()
        if len(data_str) > 0 and is_email(data_str):
            encoded_list.append(
                base64_encode(hash_sha256(normalize_email_string(data_str))))

    # Write to destination bucket.
    buffer = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")
    for encoded in random_sort(encoded_list):
        buffer.write("{}\n".format(encoded))
    buffer.seek(0)
    s3.put_object(Bucket=os.environ['destination_bucket'],
                  Key=key,
                  Body=buffer.read())

    return {"statusCode": 200}


# Determine if the string is a email address.
def is_email(data):
    if data.count('@') != 1:
        return False
    _, domain = data.split('@')
    if domain.count('.') != 1:
        return False
    return True


# Normalise email string.
def normalize_email_string(email):
    # Remove leading and trailing spaces.
    email = email.strip()
    # Convert to lowercase.
    email = email.lower()
    # In gmail.com addresses only.
    if email.endswith('@gmail.com'):
        local, domain = email.split('@')
        # Remove all dots.
        local = local.replace('.', '')
        # Remove everything after the first plus sign.
        local = local.split('+')[0]
        email = local + '@' + domain
    return email


# Base64 encode.
def base64_encode(b):
    return base64.b64encode(b).decode()


# Hash with SHA256.
def hash_sha256(data):
    return hashlib.sha256(data.encode()).digest()


# Randomly sort list.
def random_sort(list):
    for i in range(len(list)):
        j = random.randint(0, i)
        list[i], list[j] = list[j], list[i]
    return list
