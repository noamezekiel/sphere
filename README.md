![bulid status](https://travis-ci.org/noamezekiel/sphere.svg?branch=master)
![codecov](https://codecov.io/gh/noamezekiel/sphere/branch/master/graph/badge.svg)
# Sphere
Sphere is a Python library that implements a Brain Command Interface system.

## Installation
1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:noamezekiel/sphere.git
    ...
    $ cd sphere/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [sphere] $ # now you can start the fun!
    ```

We assume that docker is already installed and that it's version is > 19.03.9

## Usage
Our library consists the followings parts: client, server, parsers, saver, api, cli and gui.
### client
The client read the sample and upload it to the server.
It is available as **sphere.client** and expose the following API:


With python:
```pycon
>>> from sphere.client import upload_sample
>>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
... # upload path to the server at host:port
```
With the command-line interface:
```sh
$ python -m sphere.client upload_sample  \
      -h/--host '127.0.0.1'             \
      -p/--port 8000                    \
      'sample.mind.gz'
... # upload 'snapshot.mind.gz' to the server at host:port
```
**upload_sample** also take an optional parameter *file_format* for future samples formats.

### server
The server accept connections from clients receive the uploaded samples and publish them to its message queue.

It is available as **sphere.server** and expose the following API:

With python:
```pycon
>>> from cortex.server import run_server
>>> def print_message(message):
...     print(message)
>>> run_server(host='127.0.0.1', port=8000, publish=print_message)
... # listen on host:port and pass received messages to publish
```
With the command-line interface:
```sh
$ python -m cortex.server run-server \
      -h/--host '127.0.0.1'          \
      -p/--port 8000                 \
      'rabbitmq://127.0.0.1:5672/' # format of th url: mq_server://host:port/
... # listen on host:port and pass received messages to message queue
```
Please note that in python you can pass any publishing function, but in the cli you can only pass a URL to a message queue.