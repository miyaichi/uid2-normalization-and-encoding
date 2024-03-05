# Data processing service for Unified ID 2.0

## Introduction

With the rise of [Unified ID 2.0](https://unifiedid.com/), the need to handle customer email addresses and phone numbers through hashing has increased. This service offers a solution by normalizing, hashing, and encoding functionalities for uploaded email addresses or phone numbers.

## Features

- Perform normalization, hashing, and encoding of email addresses or phone numbers in one step.
- Automatically deletes uploaded and converted files after a default period of one hour to ensure privacy.
- Anonymity of encoded files by not including the original file name and randomizing the order of the data (so that they cannot be easily matched).

## How to Use

1. Request a form for uploading files by sending a GET request to the upload endpoint.
2. Upload a text file with one email address or phone number per line through the form.
3. Click on the download link for the encoded file provided to begin downloading. The download link will become invalid after the time (minutes) specified in expires_in in config.yml.

## Live Demo

You can try the live demo.

- [Japanese](https://ym5yz9cq41.execute-api.ap-northeast-1.amazonaws.com/dev/eventUpload/upload_file_to_s3)
- [English](https://ym5yz9cq41.execute-api.ap-northeast-1.amazonaws.com/dev/eventUpload/upload_file_to_s3?region_code=en)

## System Configuration

![uid2-normalization-and-encoding](https://github.com/miyaichi/uid2-normalization-and-encoding/assets/129797/0a55eb88-fdcd-45b0-a257-e6147a5fea2e)

## Deployment Guide

The steps to deploy a service using the serverless framework, including installing the necessary packages, cloning the repository, and configuring before deployment, are as follows:

1. Install the serverless framework with additional serverless-python-requirements.

   ```bash
   npm install -g serverless
   npm install --save serverless-python-requirements
   ```

2. Clone this repository.

   ```bash
   git clone https://github.com/miyaichi/uid2-normalization-and-encoding.git
   ```

3. Move the directory.

   ```bash
   cd uid2-normalization-and-encoding
   ```

4. Create config.yml and write your configuration.

   ```bash
   cp config.yml.sample config.yml
   ```

5. Deploy.

   ```bash
   sls deploy
   ```

## Configuration Details

You can specify the deployment region, region code, bucket name for uploaded and encoded files, and the file expiration date (in minutes).

- **region**: Specify the AWS region to deploy to.
- **region_code**: Specifies the region code in ISO 3166-1 alpha-2 format. This value is used to normalize phone numbers and select the template file's language.
- **source_bucket**: Specify the bucket's name where the uploaded files will be stored. Create a dedicated bucket to delete files periodically.
- **destination_bucket**: Specify the bucket's name where encoded files are stored. Please create a dedicated bucket to delete files periodically. Also, specify a different bucket from source_bucket.
- **expires_in**: Specify the minutes to delete files stored in source_bucket and destination_bucket. The default is 60 minutes.

The following is an example of a configuration file.

```yaml
region: ap-northeast-1
region_code: jp
source_bucket: uid2-normalization-and-encoding-source
destination_bucket: uid2-normalization-and-encoding-destination
expires_in: 60
```

## Processing Details

Follows the Unified ID 2.0 [Normalization and Encoding](https://unifiedid.com/docs/getting-started/gs-normalization-encoding) specification.

- **Normalization**: Conforms to Unified ID 2.0 specifications, including trimming, lowercase conversion, and specific address adjustments in the gmail.com domain in the case of email addresses.
- **Hashing**: Utilizes SHA-256 for hashing normalized data.
- **Encoding**: Applies Base64 encoding to the hashed values.

## Examples

The following table provides examples of input data, normalized data, and hashed and encoded output.

| email                  | normalized email      | hash and encoded                             |
| ---------------------- | --------------------- | -------------------------------------------- |
| jane.doe@gmail.com     | janedoe@gmail.com     | 1hFzBkhe0OUK+rOshx6Y+BaZFR8wKBUn1j/18jNlbGk= |
| janedoe+home@gmail.com | janedoe@gmail.com     | 1hFzBkhe0OUK+rOshx6Y+BaZFR8wKBUn1j/18jNlbGk= |
| JANESaoirse@gmail.com  | janesaoirse@gmail.com | ku4mBX7Z3qJTXWyLFB1INzkyR2WZGW4ANSJUiW21iI8= |
| user@example.com       | user@example.com      | tMmiiTI7IaAcPpQPFQ65uMVCWH8av9jw4cwf/F5HVRQ= |

| phone number (resion code) | normalized phone number | hash and encoded                             |
| -------------------------- | ----------------------- | -------------------------------------------- |
| 09012345678 (JP)           | +819012345678           | 1hFzBkhe0OUK+rOshx6Y+BaZFR8wKBUn1j/18jNlbGk= |
| 090-1234-5678 (JP)         | +819012345678           | 1hFzBkhe0OUK+rOshx6Y+BaZFR8wKBUn1j/18jNlbGk= |
| 03-1234-5678 (JP)          | +81312345678            | ku4mBX7Z3qJTXWyLFB1INzkyR2WZGW4ANSJUiW21iI8= |
| 042-123-4567 (JP)          | +81421234567            | tMmiiTI7IaAcPpQPFQ65uMVCWH8av9jw4cwf/F5HVRQ= |

# Lisence

This project is licensed under the MIT License; see the LICENSE.txt file for details.
