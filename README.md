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

```pycon
>>> from sphere.client import upload_sample
>>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
... # upload path to the server at host:port
```
And With the command-line interface:
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

```pycon
>>> from sphere.server import run_server
>>> def print_message(message):
...     print(message)
>>> run_server(host='127.0.0.1', port=8000, publish=print_message)
... # listen on host:port and pass received messages to publish
```
And with the command-line interface:
```sh
$ python -m sphere.server run-server \
      -h/--host '127.0.0.1'          \
      -p/--port 8000                 \
      'rabbitmq://127.0.0.1:5672/' # format of the url: mq_server://host:port/
... # listen on host:port and pass received messages to message queue
```
Please note that in python you can pass any publishing function, but in the cli you can only pass a URL to a message queue.

### parsers
The parsers consume raw data of a snapshot and return the parsed data.

It is available as **sphere.parsers** and expose the following API:

For running the parser on a specific data-
```pycon
>>> from sphere.parsers import run_parser
>>> data = … 
>>> result = run_parser('pose', data)
```
Which accepts a parser name and some raw data.

With the command-line interface:
```sh
$ python -m sphere.parsers parse 'pose' 'snapshot.raw' > 'pose.result'
```
Which accepts a parser name and a path to some raw data.

For running the parser as a service-
```sh
$ python -m sphere.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'
```
Which accepts a parser name and a url.
The format of the url is: *mq_server://host:port/*

### saver
The saver consumes from the message queue and saves the data to the database

It is available as **sphere.saver** and expose the following API:
```pycon
>>> from sphere.saver import Saver
>>> saver = Saver(database_url)
>>> data = …
>>> saver.save('pose', data)
```
Which connects to a database, accepts a topic name and some data, as consumed from the message queue, and saves it to the database.
The format of the url is: *db_server://host:port/*

And with the command-line interface:
```sh
python -m sphere.saver save                     \
      -d/--database 'mongodb://127.0.0.1:27017' \
     'pose'                                       \
     'pose.result' 
```
Which accepts a topic name and a path to some raw data, as consumed from the message queue, and saves it to a database.
The format of the url is the same as above.

For running the saver as a server:
```sh
$ python -m sphere.saver run-saver  \
      'mongodb://127.0.0.1:27017' \
      'rabbitmq://127.0.0.1:5672/'
```
Which consumes the data from the message queue and saves it to the database.
The format of the urls is the same as before.

### api
The api serves a RESTfull API.
It is available as **sphere.api** and expose the following API:
```pycon
>>> from sphere.api import run_api_server
>>> run_api_server(
...     host = '127.0.0.1',
...     port = 5000,
...     database_url = 'mongodb://127.0.0.1:27017',
... )
# listen on host:port and serve data from database_url
```
And with the command-line interface:
```sh
$ python -m sphere.api run-server \
      -h/--host '127.0.0.1'       \
      -p/--port 5000              \
      -d/--database 'mongodb://127.0.0.1:27017'
```
The format of the urls is the same as above.
The api server support the following RESTful API endpoints:
- **GET /users**: Returns the list of all the supported users.
- **GET /users/user-id**: Returns the specified user's details.
- **GET /users/user-id/snapshots**: Returns the list of the specified user's snapshot.
- **GET /users/user-id/snapshots/snapshot-id**: Returns the specified snapshot's details.
- **GET /users/user-id/snapshots/snapshot-id/result-name**: Returns the specified snapshot's result.
- **GET /users/user-id/snapshots/snapshot-id/color-image/data**: Data of large binary result.

### cli
The cli consume the api, and reflect it.
It is available as **sphere.cli** and expose the following cli:
```sh
$ python -m sphere.cli get-users
... # Returns the list of all the supported users
$ python -m sphere.cli get-user 1
... # Returns the details of user 1
$ python -m sphere.cli get-snapshots 1
... # Returns the list of snapshots of user 1
$ python -m sphere.cli get-snapshot 1 2
... # Returns details of snapshot 2 of user 1
$ python -m sphere.cli get-result 1 2 'pose'
... # Returns the result of snapshot 2 of user 1
```
All commands accept the *-h/--host* and *-p/--port* flags to configure the host and port, but default to the api's address.
The get-result command also accept the *-s/--save* flag that, if specified, receives a path, and saves the result's data to that path.

