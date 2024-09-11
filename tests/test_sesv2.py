import os
import unittest

from yc_aws_wrapper.sesv2 import SESV2


def order(number):
    def decorator(func):
        setattr(func, "order", number)
        return func

    return decorator


class TestSQS(unittest.TestCase):
    sesv2 = SESV2()
    mail = os.getenv("MAIL_TO", "foo@exemple.com")
    title = "Test"
    message = "Hellow world"

    @classmethod
    def sortTestMethodsUsing(cls, pre, then):
        return getattr(cls, pre).order - getattr(cls, then).order

    @order(1)
    def test_send(self):
        response = self.sesv2.foo.send(to=self.mail, title=self.title, message=self.message)
        self.assertEqual(200, response["ResponseMetadata"]["HTTPStatusCode"])


unittest.TestLoader.sortTestMethodsUsing = TestSQS.sortTestMethodsUsing
