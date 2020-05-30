from pymongo import MongoClient
import datetime as dt


class Driver():
    """ The mongodb Driver.
    :param host: The mongodb host address
    :type host: str
    :param port: The mongodb port number
    :type port: int
    """ 
    def __init__(self, host, port):
        """ Constructor method
        """
        client = MongoClient(host, port)
        self._db = client['db']
        self._users = self._db['users']

    def __repr__(self):
        return f'mongodb Driver(host={self.host}, port={self.port})'

    def save(self, topic, data):
        """ Saves data of that topic.
        :param topic: The topic of the data
        :type topic: str
        :param data: The data
        :type data: :class:`object`
        """
        if topic == 'users':
            data['birthday'] = dt.datetime.fromtimestamp(data['birthday'])
            self._users.update(
                {'user_id': data['user_id']},
                {'$set': data},
                upsert=True)
        else:
            user_id = data['user_id']
            data['snapshot_id'] = data['datetime']
            data['datetime'] = dt.datetime.fromtimestamp(data['datetime'] / 1000)
            self._db[str(user_id)].update(
                {'snapshot_id': data['snapshot_id']},
                {'$set': data},
                upsert=True)

    def get_users(self, user_id=None):
        """ Returns a list of all supported users. If user_id is mentioned, returns the specified user's details
        :param user_id: The id of the requested user, defaults to None
        :type user_id: int, optional
        :return: List of dictionaries that describes the user, or a single dictionary.
        :rtype: list, dictionary
        """ 
        if user_id:
            return self._users.find_one({'user_id': user_id}, {'_id': False})
        return list(self._users.find({}, {'_id': False}))

    def get_snapshots(self, user_id, snapshot_id=None):
        """ Returns the list of the specified user's snapshot. If snapshot_id is mentioned, returns the specified snapshot's.
        :param user_id: The id of the requested user
        :type user_id: int
        :param snapshot_id: The id of the requested snapshot
        :type snapshot_id: int, optional
        :return: List of dictionaries that describes the snapshots, or a single dictionary.
        :rtype: list, dictionary
        """ 
        snapshots_col = self._db[str(user_id)]
        if snapshot_id:
            return snapshots_col.find_one({'snapshot_id': snapshot_id}, {'_id': False})
        return list(snapshots_col.find({}, {'_id': False}))