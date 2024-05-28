import hashlib
import os
import unittest

from yc_aws_wrapper.sqs import SQS


def order(number):
    def decorator(func):
        setattr(func, "order", number)
        return func

    return decorator


class ReceptHandler:
    key = None


class TestSQS(unittest.TestCase):
    queue = os.getenv("SQS_TUBE_FOO")
    sqs = SQS()
    message = "Hellow world"
    receipt = ReceptHandler()

    @classmethod
    def sortTestMethodsUsing(cls, pre, then):
        return getattr(cls, pre).order - getattr(cls, then).order

    @classmethod
    def setUpClass(cls):
        cls.sqs.client.create_queue(QueueName=cls.queue)

    @order(1)
    def test_get_queue(self):
        queue_url = self.sqs.get_url(self.queue)
        self.assertIsNotNone(queue_url)

    @order(2)
    def test_send(self):
        hasher = hashlib.md5()
        hasher.update(self.message.encode())
        response = self.sqs.foo.send(message="Hellow world")
        self.assertEqual(hasher.hexdigest(), response.get("MD5OfMessageBody", None))

    @order(3)
    def test_receive(self):
        messages = self.sqs.foo.receive(wait=20)
        if len(messages) > 0:
            hasher = hashlib.md5()
            hasher.update(self.message.encode())
            self.receipt.key = messages[0].get("ReceiptHandle", None)
            self.assertEqual(hasher.hexdigest(), messages[0].get("MD5OfBody", None))
        else:
            self.assertTrue(False)

    @order(4)
    def test_delete_message(self):
        if self.receipt.key is not None:
            response = self.sqs.foo.delete_message(receipt=self.receipt.key)
            self.assertTrue(response)
        else:
            self.assertTrue(False)

    @order(5)
    def test_load_all_clients(self):
        os.environ.setdefault("SQS_TUBE_FOO2", os.getenv("SQS_TUBE_FOO"))
        os.environ.setdefault("SQS_TUBE_FOO3", os.getenv("SQS_TUBE_FOO"))
        if "foo2" not in self.sqs and "foo3" not in self.sqs:
            self.sqs.load_all_clients()
        else:
            self.assertTrue(False)
        self.assertTrue("foo2" in self.sqs and "foo3" in self.sqs)

    @classmethod
    def tearDownClass(cls):
        cls.sqs.client.delete_queue(QueueUrl=cls.sqs.get_url(queue=cls.queue))
        os.environ.pop("SQS_TUBE_FOO2")
        os.environ.pop("SQS_TUBE_FOO3")


unittest.TestLoader.sortTestMethodsUsing = TestSQS.sortTestMethodsUsing
