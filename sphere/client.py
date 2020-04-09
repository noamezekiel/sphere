import socket
from datetime import datetime
from .utils import Connection
from .utils import protocol
from .thought import Thought



def upload_thought(address, user_id, thought):
    timestamp = datetime.today()
    thg = Thought(user_id, timestamp, thought)
    s = socket.socket()
    s.connect(address)
    conn = Connection(s)
    conn.send(thg.serialize())
    conn.close()
    return 'done'