import flask
from furl import furl
from .. import db_drivers

app = flask.Flask('api-server')

@app.route('/users', methods=['GET'])
def get_users():
    """
    Returns the list of all the supported users, including their IDs and names only. In json format.
    
    :return: a list of dictionaries with the keys: 'user_id', 'username'
    :rtype: json
    """
    users = app._db_driver.get_users()
    data = [{'user_id': user['user_id'], 'username': user['username']} \
            for user in users]
    return flask.jsonify(data), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Returns the specified user's details: ID, name, birthday and gender. In json format.
    
    :param user_id: The id of the requested user
    :type user_id: int
    :return: Dictionary with the keys: 'user_id', 'username', 'birthday', 'gender'
    :rtype: json
    """
    user = app._db_driver.get_users(user_id=user_id)
    if not user:
        return 'user not found', 404
    return flask.jsonify(user), 200

@app.route('/users/<int:user_id>/snapshots', methods=['GET'])
def get_snapshots(user_id):
    """
    Returns the list of the specified user's snapshot IDs and datetimes. In json format.
    
    :param user_id: The id of the requested user
    :type user_id: int
    :return: List of dictionaries with the keys: 'snapshot_id', 'datetime'
    :rtype: json
    """
    snapshots = app._db_driver.get_snapshots(user_id=user_id)
    data = [{'snapshot_id': d['snapshot_id'], 
            'datetime': d['datetime']} for d in snapshots]
    return flask.jsonify(data)

@app.route('/users/<int:user_id>/snapshots/<int:snapshot_id>', methods=['GET'])
def get_snapshot(user_id, snapshot_id):
    """
    Returns the specified snapshot's details: ID, datetime, and the available results. In json format.
    
    :param user_id: The id of the requested user
    :type user_id: int
    :param snapshot_id: The id of the requested snapshot
    :type snapshot_id: int
    :return: Dictionary with the keys: 'snapshot_id', 'datetime', 'results'
    :rtype: json
    """
    snapshot = app._db_driver.get_snapshots(
        user_id=user_id,
        snapshot_id=snapshot_id)
    if not snapshot:
        return 'snapshot not ound', 404
    data = {'results': [], 'snapshot_id': snapshot['snapshot_id']}
    for key in snapshot.keys():
        if key == 'datetime':
            data[key] = snapshot[key]
        else:
            data['results'].append(key)
    return flask.jsonify(data), 200

@app.route(
    '/users/<int:user_id>/snapshots/<int:snapshot_id>/<string:result>',
    methods=['GET'])
def get_result(user_id, snapshot_id, result):
    """
    Returns the specified snapshot's result. If the result is a large binary data, returns a URL to the data.
    
    :param user_id: The id of the requested user
    :type user_id: int
    :param snapshot_id: The id of the requested snapshot
    :type snapshot_id: int
    :param result: The name of the result
    :type result: str
    :return: Dictionary with the key: result
    :rtype: json
    """
    snapshot = app._db_driver.get_snapshots(
        user_id=user_id,
        snapshot_id=snapshot_id) 
    if not snapshot:
        return 'snapshot not found', 404
    if not result.replace('-', '_') in snapshot:
        return 'result not found', 404
    if result == 'color-image' or result == 'depth-image':
        return flask.jsonify(
            {result: f'/users/{user_id}/snapshots/{snapshot_id}/{result}/data'}), 200
    return flask.jsonify({result: snapshot[result.replace('-', '_')]})

@app.route(
    '/users/<int:user_id>/snapshots/<int:snapshot_id>/<string:result>/data',
    methods=['GET'])
def get_result_data(user_id, snapshot_id, result):
    """
    Returns a large binary result in a jpg format
    
    :param user_id: The id of the requested user
    :type user_id: int
    :param snapshot_id: The id of the requested snapshot
    :type snapshot_id: int
    :param result: The name of the result
    :type result: str
    :return: The large binary data
    :rtype: file
    """
    snapshot = app._db_driver.get_snapshots(
        user_id=user_id,
        snapshot_id=snapshot_id) 
    if not snapshot:
        return 'snapshot not found', 404
    if not result.replace('-', '_') in snapshot:
        return 'result not found', 404
    if result == 'color-image' or result == 'depth-image':
        result = result.replace('-', '_')
        path = snapshot[result]
        return flask.send_file(
            path,
            attachment_filename=f'{result}.jpg',
            mimetype='image/jpg')
    return 'result has no data', 404



def run_api_server(host='0.0.0.0', port=5000, database_url='mongodb://0.0.0.0:27017/'):
    """
    Runs the API server on host, port
    
    :param host: The API host address, defaults to '0.0.0.0'
    :type host: str
    :param port: The API port number, defaults to 5000
    :type port: int
    :param database_url: The URL of the database, in the format: ``db_name://host:port/``. Defaults to `mongodb://0.0.0.0:27017/`
    :type database_url: str
    """
    f = furl(database_url)
    db, db_host, db_port = f.scheme, f.host, f.port 
    app._db_driver = db_drivers[db].Driver(db_host, db_port)
    app.run(host=host, port=port)