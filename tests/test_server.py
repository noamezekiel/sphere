import json
from multiprocessing import Process
import time
import requests
import pytest
from sphere.server import run_server
from sphere.parsers import fields
from sphere.protocol import User, Snapshot

_USER = User(
        user_id='73',
        username='Noam Ezekiel',
        birthday=123,
        gender='m')

_SNAPSHOT = Snapshot(
                datetime=123,
                translation=[1, 2, 3],
                rotation=[1, 2, 3, 4],
                color_image=[1, 1, b'1'],
                depth_image=[1, 1, 1],
                feelings=[1, 1, 1, 1])

_HOST = '127.0.0.1'
_PORT = 1234

def test_server():
    server = Process(target=run_server, args=(_HOST, _PORT))
    server.start()
    time.sleep(0.5)
    resp = requests.get(
        f'http://{_HOST}:{_PORT}/config',
        data=_USER.serialize()
    )
    assert resp.status_code == 200
    assert set(resp.json()['fields']) == set(fields)
    data = _SNAPSHOT.serialize(fields)
    resp = requests.post(
        f'http://{_HOST}:{_PORT}/snapshot',
        params={'user': _USER.serialize()},
        data=data
    )
    assert resp.status_code == 200
    server.terminate()