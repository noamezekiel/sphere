import json


class User():
    def __init__(self, user_id, username, birthday, gender):
        self.user_id = user_id
        self.username = username
        self.birthday = birthday
        self.gender = gender

    def __repr__(self):
        return f'User(user_id={self.user_id})'

    def serialize(self):
        d = self.__dict__.copy()
        return json.dumps(d)

    def to_publish(self):
        d = self.__dict__.copy()
        return json.dumps(d)      

    @staticmethod
    def deserialize(data):
        return User(**json.loads(data))