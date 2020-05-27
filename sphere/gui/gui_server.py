import flask
from furl import furl
from datetime import date
import pathlib
from .. import db_drivers


app = flask.Flask(__name__)

@app.route('/')
def index():
    users = app._db_driver.get_users()
    return flask.render_template('index.html', users=users)

@app.route('/<int:user_id>')
def user(user_id):
    user = app._db_driver.get_users(user_id=user_id)
    if user:
        snapshots = app._db_driver.get_snapshots(user_id=user_id)
        return flask.render_template('user.html', user=user, snapshots=snapshots)
    return 'wrong page', 404

@app.route('/<int:user_id>/<int:snapshot_id>')
def snapshot(user_id, snapshot_id):
    user = app._db_driver.get_users(user_id=user_id)
    if not user:
        return 'wrong page', 404
    snapshot = app._db_driver.get_snapshots(user_id=user_id, snapshot_id=snapshot_id)
    if not snapshot:
        return 'wrong page', 404
    return flask.render_template('snapshot.html', user=user, snapshot=snapshot)

@app.route('/uploads/<path:path>')
def download_file(path):
    return flask.send_file(
            '../../' + path,
            attachment_filename=f'{path}.jpg',
            mimetype='image/jpg')


def run_server(host='0.0.0.0', port='8080', database_url='mongodb://0.0.0.0:27017/'):
    f = furl(database_url)
    db, db_host, db_port = f.scheme, f.host, f.port 
    app._db_driver = db_drivers[db].Driver(db_host, db_port)
    app.run(host=host, port=port)