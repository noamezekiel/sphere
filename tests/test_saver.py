import pytest
from sphere import db_drivers
from sphere.saver import Saver
from sphere.protocol import User

_HOST = '127.0.0.1'
_PORT = 8000

_USER = User(
        user_id=73,
        username='Noam Ezekiel',
        birthday=123,
        gender='m')

class MockDriver:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def save(self, topic, raw_data):
        pass
        

db = lambda : None
db.__dict__['Driver'] = MockDriver



@pytest.fixture
def mock_db(monkeypatch):
    monkeypatch.setitem(db_drivers, 'test', db)

def test_saver(mock_db):
    saver = Saver(f'test://{_HOST}:{_PORT}/')
    saver.save('users', _USER.serialize())