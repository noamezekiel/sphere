import flask
import time
import threading
import pytest
from sphere.client import upload_sample
from sphere.parsers import fields
from sphere.protocol import User, Snapshot
from sphere.client.reader import Reader

_USER = User(
        user_id=73,
        username='Noam Ezekiel',
        birthday=123,
        gender='m')

_SNAPSHOTS = [Snapshot(
                datetime=123,
                translation=[1, 2, 3],
                rotation=[1, 2, 3, 4],
                color_image=[1, 1, b'0'*3],
                depth_image=[1, 1, 1],
                feelings=[1, 1, 1, 1])]

_HOST = '127.0.0.1'
_PORT = 8000

app = flask.Flask('server')
app.snapshots = 0

@app.route('/config', methods=['GET'])
def config():
    return flask.jsonify(fields=fields), 200

@app.route('/snapshot', methods=['POST'])
def snapshot():
    app.snapshots += 1
    return 200

class MockReader:
    def __init__(self, path, file_format):
        self.path = path
        self.user = _USER
        self.snapshots = _SNAPSHOTS

    def __iter__(self):
        for snapshot in self.snapshots:
            yield snapshot

@pytest.fixture
def mock_server():
    thread = threading.Thread(target=app.run, args=(_HOST, _PORT))
    thread.daemon = True
    thread.start()
    return app


@pytest.fixture
def mock_reader(monkeypatch):
    monkeypatch.setattr(Reader, '__init__', MockReader.__init__)
    monkeypatch.setattr(Reader, '__iter__', MockReader.__iter__)

def test_upload_sample(mock_reader, mock_server):
    time.sleep(0.5)
    upload_sample('path', host=_HOST, port=_PORT)
    time.sleep(0.5)
    assert mock_server.snapshots == 1