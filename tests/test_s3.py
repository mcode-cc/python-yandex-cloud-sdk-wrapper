import hashlib
import json
import os
import unittest

from yc_aws_wrapper.s3 import S3


def order(number):
    def decorator(func):
        setattr(func, "order", number)
        return func

    return decorator


class TestS3(unittest.TestCase):
    bucket = os.getenv("S3_BUCKET_FOO")
    s3 = S3()
    data = {"Name": "Test", "Service": "S3", "package": "yc-aws-wrapper"}
    file_name = os.path.join("test", "wrapper", "aws", "yc.json")
    file = bytes(json.dumps(data, indent=4).encode("utf8"))

    @classmethod
    def sortTestMethodsUsing(cls, pre, then):
        return getattr(cls, pre).order - getattr(cls, then).order

    @order(1)
    def test_serialize(self):
        self.file = self.s3.serialize(self.data, indent=4)
        if isinstance(self.file, bytes):
            self.assertTrue(True)

    @order(2)
    def test_put(self):
        if self.file is not None:
            hasher = hashlib.md5()
            hasher.update(self.file)
            response = self.s3.foo.put(key=self.file_name, body=self.file, acl="private")
            self.assertEqual(hasher.hexdigest(), str(response.get("ETag", None)).strip("\""))
        else:
            self.assertTrue(False)

    @order(3)
    def test_get(self):
        response = self.s3.foo.get(key=self.file_name)
        if response is not None:
            hasher = hashlib.md5()
            hasher.update(self.file)
            download = response["Body"]
            self.assertEqual(hasher.hexdigest(), str(response.get("ETag", None)).strip("\""))
        else:
            self.assertIsNotNone(response)

    @order(4)
    def test_deserialize(self):
        data = self.s3.deserialize(self.s3.buffer(self.data))
        self.assertTrue(isinstance(data, dict))

    @order(5)
    def test_load_all_clients(self):
        os.environ.setdefault("S3_BUCKET_FOO2", os.getenv("S3_BUCKET_FOO"))
        os.environ.setdefault("S3_BUCKET_FOO3", os.getenv("S3_BUCKET_FOO"))
        if "foo2" not in self.s3 and "foo3" not in self.s3:
            self.s3.load_all_clients()
        else:
            self.assertTrue(False)
        self.assertTrue("foo2" in self.s3 and "foo3" in self.s3)

    @classmethod
    def tearDownClass(cls) -> None:
        os.environ.pop("S3_BUCKET_FOO2", "")
        os.environ.pop("S3_BUCKET_FOO3", "")


unittest.TestLoader.sortTestMethodsUsing = TestS3.sortTestMethodsUsing
