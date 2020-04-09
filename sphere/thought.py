from datetime import datetime
import struct


class Thought:
    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        return f'Thought(user_id={self.user_id!r}, ' + \
            f'timestamp={self.timestamp!r}, ' + \
            f'thought={self.thought!r})'

    def __str__(self):
        s = self.timestamp.strftime("[%Y-%m-%d %H:%M:%S]")
        s += f' user {self.user_id}: '
        s += self.thought
        return s

    def __eq__(self, other):
        return isinstance(other, Thought) and \
            self.user_id == other.user_id and \
            self.timestamp == other.timestamp and \
            self.thought == other.thought

    def serialize(self):
        ts = int(self.timestamp.timestamp())
        data = struct.pack('LLI', self.user_id, ts, len(self.thought))
        data += self.thought.encode()
        return data

    def deserialize(data):
        user_id, timestamp = struct.unpack('LL', data[0:16])
        timestamp = datetime.fromtimestamp(timestamp)
        n = n = struct.unpack('I', data[16:20])[0]
        thought = data[20: 20 + n].decode()
        return Thought(user_id, timestamp, thought)
