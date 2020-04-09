import socket


def addr_to_format(tup):
    return f'{tup[0]}:{tup[1]}'


class Connection:
    def __init__(self, sock):
        self.sock = sock

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        self.close()

    @classmethod
    def connect(cls, host, port):
        s = socket.socket()
        s.connect((host, port))
        return cls(s)

    def __repr__(self):
        addr1 = addr_to_format(self.sock.getsockname())
        addr2 = addr_to_format(self.sock.getpeername())
        return f'<Connection from {addr1} to {addr2}>'

    def send(self, data):
        self.sock.sendall(data)

    def receive(self, size):
        data = b''
        left = size
        while left > 0:
            n = self.sock.recv(left)
            if not n:
                raise Exception
            data += n
            left = size - len(data)
        return data

    def close(self):
        self.sock.close()
