from botocore.exceptions import ClientError

from ..base import DynamicService, DynamicClient, Base
from ..exceptions import boto_exception


class S3Client(DynamicClient):
    def get(self, key: str, version: str = None):
        try:
            return self.client.get_object(Bucket=self.path, Key=key) if version is None else \
                self.client.get_object(Bucket=self.path, Key=key, VersionId=version)
        except ClientError as e:
            if boto_exception(e, "NoSuchKey"):
                return None
            raise e

    def put(self, key: str, body: bytes, **kwargs):
        return self.client.put_object(Bucket=self.path, Key=key, Body=body, **kwargs)

    def delete(self, key: str, version: str = None, mfa: str = None):
        params = {}
        if version is not None:
            params["VersionId"] = version
        if mfa is not None:
            params["MFA"] = mfa
        return self.client.delete_object(Bucket=self.path, Key=key, **params)


class S3(DynamicService, Base):
    def __init__(self, name: str = "s3", prefix: str = "BUCKET",
                 client_class=S3Client, auth: bool = True, config: dict = None):
        super().__init__(name=name, prefix=prefix, client_class=client_class, auth=auth, config=config)

    def __getattr__(self, item: str) -> S3Client:
        return super().__getattr__(item)
