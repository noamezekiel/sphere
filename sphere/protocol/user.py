import json


class User():
    """
    A User object of the protocol.
    
    :param user_id: The id of the user
    :type user_id: int
    :param username: The name of the user
    :type username: str
    :param birthday: The birthday of the user, in seconds since the Epoch
    :type birthday: int (seconds since the Epoch)
    :param gender: The gender of the user. 'm' for male, 'f' for female, 'o' for other
    :type gender: char
    """
    def __init__(self, user_id, username, birthday, gender):
        self.user_id = user_id
        self.username = username
        self.birthday = birthday
        self.gender = gender

    def __repr__(self):
        return f'User(user_id={self.user_id})'

    def serialize(self):
        """
        Returns a serialized user with json.
        
        :return: A serialized user
        :rtype: json
        """
        d = self.__dict__.copy()
        return json.dumps(d)

    def to_publish(self):
        """
        Returns a serialized user with json to publish on the message queue.
        
        :return: A serialized user
        :rtype: json
        """
        d = self.__dict__.copy()
        return json.dumps(d)      

    @staticmethod
    def deserialize(data):
        """
        Deserialize a user with json.
        
        :param data: The data to deserialize
        :type data: json
        :return: The user object
        :rtype: :class:`sphere.protocol.User`
        """
        return User(**json.loads(data))