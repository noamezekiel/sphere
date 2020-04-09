import struct
import datetime as dt
from .snapshot import Snapshot


class Reader():
    def __init__(self, path):
        self.path = path
        self.snapshots = []
        with open(path, 'rb') as f:
            self.user_id, name_length = struct.unpack('QI', f.read(12))
            self.user_name = f.read(name_length).decode()
            self.user_bd = dt.datetime.fromtimestamp(
                           struct.unpack('I', f.read(4))[0])
            self.user_gender, = struct.unpack('c', f.read(1))
            self._cur = f.tell()

    def read_next_snap(self):
        snap, size = Snapshot.load_snap(self.path, self._cur)
        self.snapshots.append(snap)
        self._cur += size

    def __iter__(self):
        for snap in self.snapshots:
            yield snap
