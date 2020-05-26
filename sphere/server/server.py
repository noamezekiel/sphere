import flask
import logging
import numpy as np
import threading
import pathlib
from ..parsers import fields
from ..protocol import User, Snapshot
from ..utils import DIRECTORY


app = flask.Flask('server')

@app.route('/config', methods=['GET'])
def config():
    user = User.deserialize(flask.request.data)
    logging.info(f'got config message from user {user.user_id}')
    logging.debug(f'details: {user}')
    return flask.jsonify(fields=fields), 200


@app.route('/snapshot', methods=['POST'])
def snapshot():
    snapshot = Snapshot.deserialize(flask.request.data)
    user = User.deserialize(flask.request.args['user'])
    logging.info(f'got snapshot {snapshot.datetime} from user {user.user_id}')
    path = pathlib.Path(DIRECTORY) / \
            'raw_data' / \
            str(user.user_id) / \
            str(snapshot.datetime)
    if not path.exists():
        path.mkdir(parents=True)
    # writing BLOBs to disk
    (path / 'color_image').write_bytes(snapshot.color_image[2])
    np.save(str(path / 'depth_image.npy'), np.array(snapshot.depth_image[2]))
    # publishing
    app._publish((user.to_publish(), snapshot.to_publish(path, user.user_id)))
    return 'ok', 200


def run_server(host='127.0.0.1', port=8000, publish=print):
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    app._publish = publish
    logging.basicConfig(level=logging.INFO)
    app.run(host=host, port=port)
