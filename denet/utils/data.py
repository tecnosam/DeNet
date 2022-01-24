import json
import time
from typing import Tuple


class Packet:
    def __init__(self, header: dict = None, body=None):
        self.header = header  # processing information
        self.body = body  # actual data

    def to_json(self) -> str:
        try:
            data = {"header": self.header, 'body': self.body}
            data = json.dumps(data)
        except json.JSONEncoder:
            data = json.dumps({"header": self.header, 'body': None})

        return data

    def dump(self) -> Tuple[bytes, bytes]:

        payload = self.to_json().encode()

        return payload, int.to_bytes(len(payload), 64, 'big')

    def get_size(self):
        return len(self.body)

    def __iter__(self):
        # will iterate over the body of the packet
        if type(self.body) == dict:
            return self.dump().__iter__()
        return self.body.__iter__()

    @staticmethod
    def load(stream: bytes):
        stream = json.loads(stream.decode())

        return Packet(**stream)


class Data:
    def __init__(self, node, sender, data: Packet):
        self.node = node  # of type node
        self.sender = sender  # of type machine
        self.data = data
        self.timestamp = time.time()

    def __repr__(self):
        return self.data.to_json()
