import json
import numpy as np
import pathlib
import pytest
from sphere.protocol import Snapshot, User
from sphere.parsers import parsers
from sphere.utils import DIRECTORY

_USER = User(
        user_id=73,
        username='Noam Ezekiel',
        birthday=123,
        gender='m')

_SNAPSHOT = Snapshot(
                datetime=123,
                translation=[1, 2, 3],
                rotation=[1, 2, 3, 4],
                color_image=[1, 1, b'0'*3],
                depth_image=[1, 1, [1]],
                feelings=[1, 1, 1, 1])
_SNAPSHOT.user_id = 73

_PATH = pathlib.Path(DIRECTORY) / \
            'raw_data' / \
            str(_USER.user_id) / \
            str(_SNAPSHOT.datetime)

_SNAPSHOT_JSON = '{"user_id": 73, ' \
                    '"datetime": 123, ' \
                    '"translation": [1, 2, 3], ' \
                    '"rotation": [1, 2, 3, 4], ' \
                    f'"color_image": [1, 1, "{_PATH}/color_image"], ' \
                    f'"depth_image": [1, 1, "{_PATH}/depth_image.npy"], ' \
                    '"feelings": [1, 1, 1, 1]}'


def test_color_image():
    if not _PATH.exists():
        _PATH.mkdir(parents=True)
    (_PATH / 'color_image').write_bytes(_SNAPSHOT.color_image[2])
    data = json.loads(parsers['color_image'](_SNAPSHOT_JSON))
    assert data['user_id'] == _SNAPSHOT.user_id
    assert data['datetime'] == _SNAPSHOT.datetime
    assert 'color_image' in data

def test_depth_image():
    if not _PATH.exists():
        _PATH.mkdir(parents=True)
    np.save(str(_PATH / 'depth_image.npy'), np.array(_SNAPSHOT.depth_image[2]))
    data = json.loads(parsers['depth_image'](_SNAPSHOT_JSON))
    assert data['user_id'] == _SNAPSHOT.user_id
    assert data['datetime'] == _SNAPSHOT.datetime
    assert 'depth_image' in data

def test_pose():
    data = json.loads(parsers['pose'](_SNAPSHOT_JSON))
    assert data['user_id'] == _SNAPSHOT.user_id
    assert data['datetime'] == _SNAPSHOT.datetime
    assert data['pose'] == {'translation': _SNAPSHOT.translation,
                            'rotation': _SNAPSHOT.rotation} 

def test_feelings():
    data = json.loads(parsers['feelings'](_SNAPSHOT_JSON))
    assert data['user_id'] == _SNAPSHOT.user_id
    assert data['datetime'] == _SNAPSHOT.datetime
    assert data['feelings'] == _SNAPSHOT.feelings
