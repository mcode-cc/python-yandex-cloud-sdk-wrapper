from ..base import Service


class Kinesis(Service):
    def __init__(self, name: str, auth: bool = False, config: dict = None):
        super().__init__(name=name, auth=auth, config=config)
        self.stream = "/{region}/{folder}/{database}/{stream}".format(
            region=self._region,
            folder=self._env("FOLDER"),
            database=self._env("DATABASE"),
            stream=self._env("STREAM_NAME")
        )

    def put(self, message, key: str = "1"):
        response = self.client.put_record(StreamName=self.stream, Data=message, PartitionKey=key)
        return response
