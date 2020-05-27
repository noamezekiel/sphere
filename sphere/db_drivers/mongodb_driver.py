from pymongo import MongoClient
import datetime as dt


class Driver():
    def __init__(self, host, port):
        client = MongoClient(host, port)
        self._db = client['db']
        self._users = self._db['users']

    def __repr__(self):
        return f'mongodb Driver(host={self.host}, port={self.port})'

    def save(self, topic, data):
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
        if user_id:
            return self._users.find_one({'user_id': user_id}, {'_id': False})
        return list(self._users.find({}, {'_id': False}))

    def get_snapshots(self, user_id, snapshot_id=None):
        snapshots_col = self._db[str(user_id)]
        if snapshot_id:
            return snapshots_col.find_one({'snapshot_id': snapshot_id}, {'_id': False})
        return list(snapshots_col.find({}, {'_id': False}))