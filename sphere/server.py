import struct
import threading
from pathlib import Path
from .utils import Listener
from .thought import Thought
import flask
from flask import request
from flask import jsonify

PARSERS = []

app = Flask('server')

@app.route('/config', methods=['GET'])
def config():
    return jsonify(parsers=PARSERS)

@app.route('/snapshot', methods=['POST'])
def snapshot():



def run_server(address, data_dir):
    global data
    data = data_dir
    app.run(*address)