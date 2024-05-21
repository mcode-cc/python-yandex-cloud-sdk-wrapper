import json
from typing import Optional, Union

from ..base import Service


class SQS(Service):
    def get_url(self, queue: str) -> Optional[str]:
        return self.client.get_queue_url(queue).get("QueueUrl", None)

    def send(self, queue: str, message: Union[dict, str], attributes: dict = None):
        params = {
            "QueueUrl": self.get_url(queue=queue),
            "MessageBody": json.dumps(message) if isinstance(message, dict) else message
        }
        if isinstance(attributes, dict):
            params["MessageAttribute"] = attributes
        return self.client.send_message(**params)

    def receive(self, queue: str, visibility: int = 60, wait: int = 0,
                max_number: int = 10,  additional: dict = None) -> list:
        """
        :param queue: Queue name
        :param visibility: The duration (in seconds) that the received messages are hidden from subsequent retrieve
            requests after being retrieved by a ReceiveMessage request.
        :param wait: The duration (in seconds) for which the call waits for a message to arrive in the queue before
            returning. If a message is available, the call returns sooner than WaitTimeSeconds. If no messages are
            available and the wait time expires, the call does not return a message list.
        :param max_number: The maximum number of messages to return. Amazon SQS never returns more messages than this
            value (however, fewer messages might be returned). Valid values: 1 to 10
        :param additional: additional params from guide boto3 -> SQS.Client.receive_message
        :return: list, dicts or empty
        """
        if not isinstance(additional, dict):
            additional = {}
        params = {
            "QueueUrl": self.get_url(queue=queue),
            "VisibilityTimeout": visibility,
            "WaitTimeSeconds": wait,
            "MaxNumberOfMessages": max_number,
            **additional
        }
        return self.client.receive_message(**params).get("Messages", [])

    def delete_message(self, queue: str, receipt: str):
        return self.client.delete_message(QueueUrl=self.get_url(queue), ReceiptHandle=receipt)
