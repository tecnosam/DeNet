from .data import Packet


class Connection:
    def __init__(self, nickname: str, ip: str, port: int, fresh=True):
        self.nickname = nickname  # nickname user is connecting as
        self.ip = ip
        self.port = port
        self.fresh = fresh

    def __str__(self):
        return f"{self.nickname},{self.ip},{self.port}"

    def to_packet(self):
        header = {'type': 'conn-info'}
        body = {'nickname': self.nickname, 'ip': self.ip, 'fresh': self.fresh}

        return Packet(header, body)
