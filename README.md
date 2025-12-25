# yc-aws-wrapper

[![License](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Development Status](https://img.shields.io/badge/status-planning-yellow.svg)](https://github.com/mcode-cc/python-yandex-cloud-sdk-wrapper)

A wrapper for convenient work with Yandex Cloud services through AWS-compatible APIs. May also be compatible with other AWS-compatible services.

## Description

`yc-aws-wrapper` provides a simplified interface for working with Yandex Cloud services (S3, SQS, SESV2, Kinesis) through the standard AWS SDK (boto3). The wrapper is written for your own needs and primarily for working with Yandex Cloud, ready for criticism and suggestions.

### Supported Services

- **S3** — Object storage
- **SQS** — Message queues
- **SESV2** — Email sending
- **Kinesis** — Data streams

## Table of Contents

- [Installation](#installation)
- [Requirements](#requirements)
- [Environment Variables](#environment-variables)
  - [Required](#required)
  - [Optional (per service)](#optional-per-service)
- [Usage](#usage)
  - [SQS — Sending and Receiving Messages](#sqs---sending-and-receiving-messages)
  - [S3 — Working with Objects](#s3---working-with-objects)
  - [SESV2 — Sending Email](#sesv2---sending-email)
  - [Kinesis — Data Streams](#kinesis---data-streams)
  - [AWS — Universal Client](#aws---universal-client)
- [Examples](#examples)
- [Testing](#testing)
- [Error Handling](#error-handling)
- [License](#license)
- [Links](#links)
- [Authors](#authors)
- [Contributing](#contributing)

## Installation

```bash
pip install yc-aws-wrapper
```

Or from source:

```bash
git clone https://github.com/mcode-cc/python-yandex-cloud-sdk-wrapper.git
cd python-yandex-cloud-sdk-wrapper
pip install -e .
```

## Requirements

- Python 3.8+
- boto3 >= 1.27.1
- botocore >= 1.30.1

## Environment Variables

### Required

```bash
AWS_REGION=ru-central1
AWS_ACCESS_KEY_ID=<your_key_id>
AWS_SECRET_ACCESS_KEY=<your_secret_key>
```

### Optional (per service)

#### Endpoint URLs

For each service, you can specify a custom endpoint:

```bash
SQS_ENDPOINT_URL=https://message-queue.api.cloud.yandex.net
S3_ENDPOINT_URL=https://storage.yandexcloud.net
SESV2_ENDPOINT_URL=https://email.api.cloud.yandex.net
KINESIS_ENDPOINT_URL=<your_endpoint>
```

#### SQS — Queues

```bash
SQS_TUBE_[METHOD_NAME]=<queue_name>
```

**Example:**
```bash
SQS_TUBE_FOO=foo-queue
SQS_TUBE_BAR=bar-queue
```

Usage: `sqs.foo.send(...)`, `sqs.bar.send(...)`

#### S3 — Buckets

```bash
S3_BUCKET_[METHOD_NAME]=<bucket_name>
```

**Example:**
```bash
S3_BUCKET_FOO=my-bucket
S3_BUCKET_BAR=another-bucket
```

Usage: `s3.foo.get(...)`, `s3.bar.put(...)`

#### SESV2 — Mailboxes

```bash
SESV2_MAILBOX_[METHOD_NAME]=<email_address>
```

**Example:**
```bash
SESV2_MAILBOX_FOO=mail@example.com
SESV2_MAILBOX_BAR=another@example.com
```

Usage: `sesv2.foo.send(...)`, `sesv2.bar.send(...)`

#### Kinesis — Data Streams

```bash
KINESIS_FOLDER=<folder_id>
KINESIS_DATABASE=<database_name>
KINESIS_STREAM_NAME=<stream_name>
```

## Usage

### SQS — Sending and Receiving Messages

```python
from yc_aws_wrapper.sqs import SQS

sqs = SQS()

# Send a message to a queue
response = sqs.foo.send("Hello World")
print(response)  # dict with result

# Send a message with attributes
response = sqs.foo.send(
    message={"key": "value"},
    attributes={"CustomAttribute": {"StringValue": "value", "DataType": "String"}}
)

# Receive messages
messages = sqs.foo.receive(visibility=60, wait=20, max_number=10)
for msg in messages:
    print(msg["Body"])
    # Delete message after processing
    sqs.foo.delete_message(receipt=msg["ReceiptHandle"])

# Work with all queues
sqs.load_all_clients()
for queue_name, queue_client in sqs:
    queue_client.send("Broadcast message")
```

### S3 — Working with Objects

```python
from yc_aws_wrapper.s3 import S3

s3 = S3()

# Get an object
response = s3.foo.get(key="path/to/file.json")
if response:
    data = response["Body"].read()
    print(data)

# Get an object with version
response = s3.foo.get(key="path/to/file.json", version="version_id")
# Note: get() returns None if the object doesn't exist (NoSuchKey error)

# Upload a file
s3.foo.put(
    key="path/to/file.json",
    body=b'{"key": "value"}',
    ContentType="application/json"
)

# Delete an object
s3.foo.delete(key="path/to/file.json")

# Delete an object version
s3.foo.delete(key="path/to/file.json", version="version_id")

# Serialization and deserialization
data = {"key": "value"}
serialized = s3.serialize(data, indent=2)  # bytes
deserialized = s3.deserialize(serialized)  # dict
buffer = s3.buffer(data)  # io.BytesIO
```

### SESV2 — Sending Email

```python
from yc_aws_wrapper.sesv2 import SESV2

sesv2 = SESV2()

# Simple send
response = sesv2.foo.send(
    to="recipient@example.com",
    title="Subject",
    message="Email body"
)

# Send to multiple recipients
response = sesv2.foo.send(
    to=["user1@example.com", "user2@example.com"],
    title="Subject",
    message="Email body"
)

# Advanced send with custom content
response = sesv2.foo.send(
    to="recipient@example.com",
    title="Subject",
    message="Email body",
    Content={
        "Simple": {
            "Subject": {"Data": "Custom Subject", "Charset": "UTF-8"},
            "Body": {
                "Text": {"Data": "Text body", "Charset": "UTF-8"},
                "Html": {"Data": "<html>HTML body</html>", "Charset": "UTF-8"}
            }
        }
    }
)
```

### Kinesis — Data Streams

```python
from yc_aws_wrapper.kinesis import Kinesis

kinesis = Kinesis(name="kinesis", auth=True)

# Send a record to the stream
response = kinesis.put(
    message=b"data",
    key="partition_key"
)
```

### AWS — Universal Client

```python
from yc_aws_wrapper import AWS

aws = AWS(name="aws")

# Access to services
aws.sqs.foo.send("message")
aws.cos.foo.get(key="file.json")
aws.kinesis.put(message=b"data", key="key")

# Load from S3 with error handling
# Note: The bucket parameter should correspond to an S3 client configured via S3_BUCKET_* env vars
response = aws.load(bucket="bucket", key="key", version=None)
if response["statusCode"] == 200:
    print("Success")
elif response["statusCode"] == 404:
    print("Not found")
```

## Examples

### Example 1: Sending Messages to Multiple Queues

```python
from yc_aws_wrapper.sqs import SQS

sqs = SQS()

# Send to queue foo (declared in ENV)
response = sqs.foo.send("Hello World")
print(type(response))  # <class 'dict'>

# Send to queue bar (declared in ENV)
response = sqs.bar.send("Hello World")
print(type(response))  # <class 'dict'>

# Try to send to baz (not declared in ENV)
response = sqs.baz.send("Hello World")
print(type(response))  # <class 'NoneType'>
```

**Environment variables:**
```bash
AWS_REGION=ru-central1
AWS_ACCESS_KEY_ID=<KEY_ID>
AWS_SECRET_ACCESS_KEY=<SECRET_KEY>
SQS_ENDPOINT_URL=https://message-queue.api.cloud.yandex.net
SQS_TUBE_FOO=foo-queue
SQS_TUBE_BAR=bar-queue
```

### Example 2: Sending to All Queues

```python
from yc_aws_wrapper.sqs import SQS

sqs = SQS()

# Load all clients from environment variables
sqs.load_all_clients()

# Send message to all queues
for queue_name, queue_client in sqs:
    queue_client.send("Hello World")
```

## Testing

To run tests, you need to set environment variables:

```bash
# Required
export AWS_REGION=ru-central1
export AWS_ACCESS_KEY_ID=<your_key>
export AWS_SECRET_ACCESS_KEY=<your_secret>

# For S3 tests
export S3_BUCKET_FOO=<your_test_bucket>

# For SQS tests
export SQS_ENDPOINT_URL=https://message-queue.api.cloud.yandex.net
export SQS_TUBE_FOO=<your_test_queue>

# For SESV2 tests
export SESV2_ENDPOINT_URL=https://email.api.cloud.yandex.net
export SESV2_MAILBOX_FOO=<your_test_email>
export MAIL_TO=<recipient_email>
```

Run tests:

```bash
python -m unittest discover tests
```

Or individual tests:

```bash
python -m unittest tests.test_s3
python -m unittest tests.test_sqs
python -m unittest tests.test_sesv2
```

## Error Handling

The library uses `Stub` objects for clients that are not configured via environment variables. These stub objects return `None` instead of raising exceptions. For handling boto3 errors, use:

```python
from botocore.exceptions import ClientError
from yc_aws_wrapper.exceptions import boto_exception

try:
    response = s3.foo.get(key="nonexistent")
except ClientError as e:
    if boto_exception(e, "NoSuchKey"):
        print("Key not found")
    else:
        raise
```

## License

This project is distributed under the [GNU Affero General Public License v3.0](LICENSE).

## Links

- [GitHub Repository](https://github.com/mcode-cc/python-yandex-cloud-sdk-wrapper)
- [Bug Reports](https://github.com/mcode-cc/python-yandex-cloud-sdk-wrapper/issues)
- [Yandex Cloud Documentation](https://cloud.yandex.ru/docs)
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## Authors

- **MCode GmbH** — [mcode-cc](https://github.com/mcode-cc)

## Contributing

Criticism and suggestions are welcome! Please create issues to discuss changes or submit pull requests.
