import base64
from functools import lru_cache

from botocore.exceptions import ClientError

from yc_aws_wrapper.base import Base
from yc_aws_wrapper.kinesis import Kinesis
from yc_aws_wrapper.s3 import S3
from yc_aws_wrapper.sqs import SQS


class AWS(Base):
    def __init__(self, name: str):
        super().__init__(name=name)
        self._kinesis = None
        self._s3 = None
        self._sqs = None

    @lru_cache(maxsize=1024)
    def load(self, bucket, key, version):
        try:
            response = self.cos.get(key, bucket, version)
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return {
                    "statusCode": 404,
                    "body": ""
                }
            else:
                raise
        headers = response["ResponseMetadata"]["HTTPHeaders"]
        if "accept-ranges" in headers:
            headers.pop("accept-ranges")
        if headers.get("content-type") == "application/json":
            headers["content-type"] = "application/json; charset=utf-8"
        return {
            "statusCode": 200,
            "body": base64.standard_b64encode(response["Body"].read()).decode(),
            "isBase64Encoded": True,
            "headers": headers
        }

    @property
    def kinesis(self):
        if self._kinesis is None:
            self._kinesis = Kinesis("kinesis", auth=True)
        return self._kinesis

    @property
    def cos(self):
        if self._s3 is None:
            self._s3 = S3("s3", auth=True)
        return self._s3

    @property
    def sqs(self):
        if self._sqs is None:
            self._sqs = SQS("sqs", auth=True)
        return self._sqs
