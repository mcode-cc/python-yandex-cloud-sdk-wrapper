from datetime import datetime

from ..base import Service


class S3(Service):
    def get(self, key: str, bucket: str, version: str = None):
        return self.client.get_object(Bucket=bucket, Key=key) if version is None else \
            self.client.get_object(Bucket=bucket, Key=key, VersionId=version)

    def put(self, key: str, bucket: str, body: bytes, acl: str = None, expires: datetime = None):
        additional = {}
        if acl is not None:
            additional["ACL"] = acl
        if isinstance(expires, datetime):
            additional["Expires"] = expires
        return self.client.put_object(Bucket=bucket, Key=key, Body=body, **additional)
