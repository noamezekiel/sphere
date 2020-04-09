from .connection import Connection
import socket


class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception, error, traceback):
        self.stop()

    def __repr__(self):
        return f'Listener(port={self.port!r}, ' + \
                f'host={self.host!r}, ' + \
                f'backlog={self.backlog!r}, ' + \
                f'reuseaddr={self.reuseaddr})'

    def start(self):
        self.sock = socket.socket()
        if self.reuseaddr:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.backlog)

    def stop(self):
        self.sock.close()

    def accept(self):
        return Connection(self.sock.accept()[0])
