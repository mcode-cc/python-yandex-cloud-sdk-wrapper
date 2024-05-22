from datetime import datetime

from botocore.exceptions import ClientError

from ..base import Service


class S3(Service):
    def get(self, key: str, bucket: str, version: str = None):
        try:
            result = self.client.get_object(Bucket=bucket, Key=key) if version is None else \
                self.client.get_object(Bucket=bucket, Key=key, VersionId=version)
        except ClientError as e:
            try:
                if e.response["Error"]["Code"] == "NoSuchKey":
                    result = None
                else:
                    raise e
            except Exception:
                raise e
        return result

    def put(self, key: str, bucket: str, body: bytes, acl: str = None, expires: datetime = None):
        params = {}
        if acl is not None:
            params["ACL"] = acl
        if isinstance(expires, datetime):
            params["Expires"] = expires
        return self.client.put_object(Bucket=bucket, Key=key, Body=body, **params)

    def delete(self, key: str, bucket: str, version: str = None, mfa: str = None):
        params = {}
        if version is not None:
            params["VersionId"] = version
        if mfa is not None:
            params["MFA"] = mfa
        return self.client.delete_object(Bucket=bucket, Key=key, **params)
