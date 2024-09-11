from typing import Union, List

import boto3
from botocore.exceptions import ClientError

from ..base import DynamicClient, DynamicService
from ..exceptions import boto_exception


class SESV2Client(DynamicClient):
    def __init__(self, client: boto3.client, path: str):
        super().__init__(client, path)

    def send(self, to: Union[str, List[str]], title, message, charset: str = "UTF-8", **kwargs):
        destination = kwargs["Destination"] if "Destination" in kwargs else {}
        destination["ToAddresses"] = [to] if isinstance(to, str) else to
        content = kwargs["Content"] if "Content" in kwargs else {}
        if len(content) < 1:
            content = {
                "Simple": {
                    "Subject": {"Data": title, "Charset": charset},
                    "Body": {"Text": {"Data": message, "Charset": charset}}
                }
            }
        elif "Simple" in content:
            content["Simple"]["Subject"] = {"Data": title, "Charset": charset}
            if "Body" not in content["Simple"]:
                content["Simple"]["Body"] = {}
            if "Html" not in content["Simple"]["Body"]:
                content["Simple"]["Body"]["Text"] = {"Data": message, "Charset": charset}
        try:
            return self.client.send_email(
                FromEmailAddress=self.path,
                Destination=destination,
                Content=content
            )
        except ClientError as e:
            if boto_exception(e, ""):
                return None
            raise e


class SESV2(DynamicService):
    def __init__(self, name: str = "sesv2", prefix: str = "MAILBOX",
                 client_class=SESV2Client, auth: bool = True, config: dict = None):
        super().__init__(name=name, prefix=prefix, client_class=client_class, auth=auth, config=config)

    def __getattr__(self, item: str) -> SESV2Client:
        return super().__getattr__(item)
