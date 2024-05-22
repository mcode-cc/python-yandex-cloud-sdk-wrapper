import io
import json
import os
from typing import Optional

import boto3
from botocore.config import Config


class Base:
    def __init__(self, name: str):
        self.name = name
        self._region = os.environ.get("AWS_REGION")
        self._key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        self._secret = os.environ.get("AWS_SECRET_ACCESS_KEY")

    def _env(self, *args, default: str = None) -> Optional[str]:
        return os.environ.get("_".join([x.upper() for x in map(str, (self.name,) + args)]), default)

    @staticmethod
    def serialize(data: dict, indent: int = None) -> bytes:
        return bytes(json.dumps(data, indent=indent).encode("utf8"))

    @staticmethod
    def deserialize(data, _type: str = "json") -> dict:
        if _type == "json":
            return json.loads(s=data) if isinstance(data, bytes) else json.load(fp=data)

    def buffer(self, data: dict, indent: int = None) -> io.BytesIO:
        result = io.BytesIO()
        result.write(self.serialize(data=data, indent=indent))
        result.seek(0)
        return result


class Service(Base):
    def __init__(self, name: str, auth: bool = True, config: dict = None):
        super().__init__(name=name)
        self.name = name
        self._auth = auth
        self._config = config
        self._client = None
        self._resource = None
        self._endpoint = self._env("ENDPOINT_URL")

    @property
    def params(self) -> dict:
        result = {
            "service_name": self.name,
            "endpoint_url": self._endpoint
        }
        if self._config is not None:
            result["config"] = Config(**self._config)
        if self._region is not None:
            result["region_name"] = str(self._region)
        if self._auth:
            result.update({"aws_access_key_id": self._key_id, "aws_secret_access_key": self._secret})
        return result

    @property
    def resource(self) -> boto3.resource:
        if self._resource is None:
            self._resource = boto3.resource(**self.params)
        return self._resource

    @property
    def client(self) -> boto3.client:
        if self._client is None:
            self._client = boto3.client(**self.params)
        return self._client
