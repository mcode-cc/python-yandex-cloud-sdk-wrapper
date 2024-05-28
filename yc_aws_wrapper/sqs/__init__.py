import json
from typing import Optional, Union

import boto3
from botocore.exceptions import ClientError

from ..base import DynamicClient, DynamicService
from ..exceptions import boto_exception


class SQSClient(DynamicClient):
    def __init__(self, client: boto3.client, path: str):
        super().__init__(client, path)
        self.queue = self.client.get_queue_url(QueueName=path).get("QueueUrl", None)

    def send(self, message: Union[dict, str], attributes: dict = None) -> dict:
        """
        :param message: MessageBody
        :param attributes: MessageAttribute
        :return: response form send
        """
        params = {
            "QueueUrl": self.queue,
            "MessageBody": json.dumps(message) if isinstance(message, dict) else message
        }
        if isinstance(attributes, dict):
            params["MessageAttribute"] = attributes
        return self.client.send_message(**params)

    def receive(self, visibility: int = 60, wait: int = 20, max_number: int = 10, **kwargs) -> list:
        """
        :param visibility: The duration (in seconds) that the received messages are hidden from subsequent retrieve
            requests after being retrieved by a ReceiveMessage request.
        :param wait: The duration (in seconds) for which the call waits for a message to arrive in the queue before
            returning. If a message is available, the call returns sooner than WaitTimeSeconds. If no messages are
            available and the wait time expires, the call does not return a message list.
        :param max_number: The maximum number of messages to return. Amazon SQS never returns more messages than this
            value (however, fewer messages might be returned). Valid values: 1 to 10
        :param kwargs: additional params from guide boto3 -> SQS.Client.receive_message
        :return: list, dicts or empty
        """

        params = {
            "QueueUrl": self.queue,
            "VisibilityTimeout": visibility,
            "WaitTimeSeconds": wait,
            "MaxNumberOfMessages": max_number,
            **kwargs
        }
        return self.client.receive_message(**params).get("Messages", [])

    def delete_message(self, receipt: str) -> bool:
        try:
            self.client.delete_message(QueueUrl=self.queue, ReceiptHandle=receipt)
            return True
        except ClientError as e:
            if boto_exception(e, "ReceiptHandleIsInvalid"):
                return False
            raise e


class SQS(DynamicService):
    def __init__(self, name: str = "sqs", prefix: str = "TUBE",
                 client_class=SQSClient, auth: bool = True, config: dict = None):
        super().__init__(name=name, prefix=prefix, client_class=client_class, auth=auth, config=config)

    def get_url(self, queue: str) -> Optional[str]:
        try:
            return self.client.get_queue_url(QueueName=queue).get("QueueUrl", None)
        except ClientError as e:
            if boto_exception(e, "QueueDoesNotExist"):
                return None
            raise e

    def __getattr__(self, item: str) -> SQSClient:
        return super().__getattr__(item)
