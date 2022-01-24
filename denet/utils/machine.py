from socket import socket
from datetime import datetime

class Machine:
    def __init__(self, nickname: str, address: tuple, client: socket, meta: list = None):
        self.nickname = nickname
        self.ip, self.port = address
        self.client = client
        self.active = True
        self.meta = meta  # metadata of Machine, additional logs to be kept
        self.last_updated = datetime.utcnow()
        self.last_broadcast = []

    def to_dict(self):
        return {'nickname': self.nickname, 'ip': self.ip}

    def __str__(self):
        return f"{self.nickname},{self.ip},{self.port}"

    def __bytes__(self):
        return self.__str__().encode()
