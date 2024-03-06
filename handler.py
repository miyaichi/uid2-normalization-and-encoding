""" Lambda function for the File Upload to S3 and Data Normalization and Encoding. """
import base64
import cgi
import datetime
import hashlib
import io
import logging
import os
import random
import uuid

import boto3
import jinja2
import phonenumbers
from botocore.config import Config

# -*- coding: utf-8 -*-

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def upload_file_to_s3(event: dict, _context: dict) -> dict:
    """
    Uploads a file to S3 and returns an HTML form for file upload.

    Args:
        event (dict): The event data.
        _context (dict): The context data.

    Returns:
        dict: The response containing the HTML form or an error message.
    """
    logger.info("File upload request.")

    # Initialize S3 and Jinja2 environment.
    s3_client = boto3.client('s3',
                             config=Config(
                                 region_name=os.environ["AWS_REGION"],
                                 signature_version="s3v4"))
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(
        searchpath="./templates"))

    # Get region code parameter.
    region_code = os.environ["region_code"]
    try:
        region_code = event.get("queryStringParameters",
                                {}).get("region_code", region_code)
    except:
        pass

    if event["httpMethod"] == "GET":
        try:
            # Send the upload form.
            template = environment.get_template(f"upload-{region_code}.tpl")
            return {
                "statusCode":
                200,
                "headers": {
                    "Content-Type": "text/html"
                },
                "body":
                template.render({
                    "expires_in": os.environ["expires_in"],
                    "region_code": region_code,
                    "region": os.environ["AWS_REGION"],
                    "domain": event["requestContext"]["domainName"],
                    "stage": event["requestContext"]["stage"],
                    "path": event["requestContext"]["resourcePath"]
                })
            }
        except Exception as error:
            return {
                "statusCode":
                500,
                "body":
                f"An error occurred while rendering the template: {str(error)}"
            }

    if event["httpMethod"] == "POST":
        # Generate unique keys using uuid.
        key = str(uuid.uuid4()) + ".csv"

        data_type = "email"
        try:
            # Parse multi-part data.
            _, c_data = cgi.parse_header(event["headers"]["content-type"])
            c_data["boundary"] = bytes(c_data["boundary"], "utf8")
            form_data = cgi.parse_multipart(
                io.BytesIO(bytes(event["body"], "utf8")), c_data)

            # Get data_type parameter.
            data_type = form_data.get("data_type", [data_type])[0]
        except Exception as error:
            return {
                "statusCode":
                400,
                "body":
                f"An error occurred while parsing the multi-part data: {str(error)}"
            }

        try:
            # Store in S3.
            header = data_type.encode() + b"\n"
            data = header + form_data["file"][0]
            s3_client.put_object(Bucket=os.environ["source_bucket"],
                                 Key=key,
                                 Body=data)

            # Generate a pre-signed URL.
            location = s3_client.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": os.environ["destination_bucket"],
                    "Key": key
                },
                ExpiresIn=int(os.environ["expires_in"]) * 60,
                HttpMethod="GET")

            # Returns a link to download a file.
            template = environment.get_template(f"download-{region_code}.tpl")
            return {
                "statusCode":
                200,
                "headers": {
                    "Content-Type": "text/html"
                },
                "body":
                template.render({
                    "key": key,
                    "location": location,
                    "expires_in": os.environ["expires_in"]
                })
            }
        except Exception as error:
            return {
                "statusCode":
                500,
                "body":
                f"An error occurred while storing the file in S3: {str(error)}"
            }

    return {"statusCode": 400, "body": "Invalid request."}


def clean_up_buckets(_event: dict, _context: dict) -> dict:
    """
    Cleans up the source and destination buckets by deleting expired objects.

    Args:
        _event (dict): The event data.
        _context (dict): The context data.

    Returns:
        dict: The response indicating the success or failure of the cleanup operation.
    """
    logger.info("Clean up source and destination bucket.")

    # Initialize S3.
    s3_client = boto3.client('s3',
                             config=Config(
                                 region_name=os.environ["AWS_REGION"],
                                 signature_version="s3v4"))

    # Expires_in minutes before current time.
    date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
        minutes=int(os.environ["expires_in"]))

    # Scan buckets and delete old objects.
    buckets = [os.environ["source_bucket"], os.environ["destination_bucket"]]
    for bucket in buckets:
        response = s3_client.list_objects_v2(Bucket=bucket)
        if "Contents" in response:
            for obj in response["Contents"]:
                last_modified = obj["LastModified"]
                key = obj["Key"]
                if last_modified < date:
                    try:
                        # Delete expired object.
                        s3_client.delete_object(Bucket=bucket, Key=key)
                        logger.info(
                            "Deleted Key %s in Bucket %s (last_modified: %s).",
                            key, bucket, last_modified)
                    except Exception as error:
                        logger.error(
                            f"An error occurred while deleting Key %s in Bucket %s: {str(error)}",
                            key, bucket)

    return {"statusCode": 200}


def normalization_and_encoding(event: dict, _context: dict) -> dict:
    """
    Normalizes and encodes email addresses in S3 bucket files.

    Args:
        event (dict): The event data.
        _context (dict): The context data.

    Returns:
        dict: The response indicating the success or failure of the normalization and encoding.
    """
    logger.info("New files uploaded to the source bucket.")

    # Initialize S3.
    s3_client = boto3.client('s3',
                             config=Config(
                                 region_name=os.environ["AWS_REGION"],
                                 signature_version="s3v4"))

    try:
        source_bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = event["Records"][0]["s3"]["object"]["key"]
        logger.info("source: %s, key: %s", source_bucket, key)

        # Process the file.
        source = s3_client.get_object(Bucket=source_bucket, Key=key)
        region_code = os.environ["region_code"].upper()
        data_type = "email"
        encoded_list = []
        for line in source["Body"]._raw_stream:
            data_str = line.decode("utf-8").rstrip()
            # Skip empty lines.
            if len(data_str) == 0:
                continue

            # check if the first line is a header.
            if data_str.lower() == "email" or data_str.lower() == "phone":
                data_type = data_str.lower()
                continue

            # Process email addresses.
            if data_type == "email" and is_email(data_str):
                encoded_list.append(
                    base64_encode(hash_sha256(
                        normalize_email_string(data_str))))
            # Process phone numbers.
            elif data_type == "phone" and is_phone_number(
                    data_str, region_code):
                encoded_list.append(
                    base64_encode(
                        hash_sha256(
                            normalize_phone_number(data_str, region_code))))
    except Exception as error:
        return {
            "statusCode": 500,
            "body":
            f"An error occurred while processing the file: {str(error)}"
        }

    try:
        destination_bucket = os.environ["destination_bucket"]
        logger.info("destination: %s, key: %s", destination_bucket, key)

        # Write to destination bucket.
        buffer = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")
        for encoded in random_sort(encoded_list):
            buffer.write(f"{encoded}\n")
        buffer.seek(0)
        s3_client.put_object(Bucket=destination_bucket,
                             Key=key,
                             Body=buffer.read())
    except Exception as error:
        return {
            "statusCode":
            500,
            "body":
            f"An error occurred while storing the file in the destination bucket: {str(error)}"
        }

    return {"statusCode": 200}


def is_email(data: str) -> bool:
    """
    Determines if the string is an email address.

    Args:
        data (str): The string to check.

    Returns:
        bool: True if the string is an email address, False otherwise.
    """
    if data.count("@") != 1:
        return False
    _, domain = data.split("@")
    if domain.count(".") != 1:
        return False
    return True


def normalize_email_string(email: str) -> str:
    """
    Normalizes an email string.

    Args:
        email (str): The email string to normalize.

    Returns:
        str: The normalized email string.
    """
    # Remove leading and trailing spaces.
    email = email.strip()
    # Convert to lowercase.
    email = email.lower()
    # In gmail.com addresses only.
    if email.endswith("@gmail.com"):
        local, domain = email.split("@")
        # Remove all dots.
        local = local.replace(".", "")
        # Remove everything after the first plus sign.
        local = local.split("+")[0]
        email = local + "@" + domain
    return email


def is_phone_number(phone: str, region_code: str) -> bool:
    """
    Determines if the string is a phone number.

    Args:
        phone (str): The string to check.
        region_code (str): The region code of the phone number.

    Returns:
        bool: True if the string is a phone number, False otherwise.
    """
    try:
        phonenumbers.parse(phone, region_code)
        return True
    except phonenumbers.phonenumberutil.NumberParseException:
        return False


def normalize_phone_number(phone: str, region_code: str) -> str:
    """
    Normalizes a phone number string.

    Args:
        phone (str): The phone number string to normalize.
        region_code (str): The region code of the phone number.

    Returns:
        str: The normalized phone number string.
    """
    try:
        phone = phonenumbers.format_number(
            phonenumbers.parse(phone, region_code),
            phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.phonenumberutil.NumberParseException:
        phone = ""
    return phone


def base64_encode(data: bytes) -> str:
    """
    Encodes bytes using Base64.

    Args:
        data (bytes): The bytes to encode.

    Returns:
        str: The Base64 encoded string.
    """
    return base64.b64encode(data).decode()


def hash_sha256(data: str) -> bytes:
    """
    Hashes a string using SHA256.

    Args:
        data (str): The string to hash.

    Returns:
        bytes: The hashed bytes.
    """
    return hashlib.sha256(data.encode()).digest()


def random_sort(lst: list) -> list:
    """
    Randomly sorts a list.

    Args:
        lst (list): The list to sort.

    Returns:
        list: The randomly sorted list.
    """
    for i, _ in enumerate(lst):
        j = random.randint(0, i)
        lst[i], lst[j] = lst[j], lst[i]
    return lst
