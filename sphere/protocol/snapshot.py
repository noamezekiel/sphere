import bson
import json
import pathlib


class Snapshot():
    """
    A Snapshot object of the protocol.
    
    :param datetime: The datetime of the snapshot, in milliseconds since the Epoch
    :type datetime: int (milliseconds since the Epoch)
    :param translation: A list of 3 coordinates
    :type translation: list
    :param rotation: A list of 4 coordinates
    :type rotation: list
    :param color_image: A list, with first element as width, second as hight and third as bytes
    :type color_image: list
    :param depth_image: A list, with first element as width, second as hight and third as floats
    :type depth_image: list
    :param feelings: A list of 4 values between -1 to 1: hunger, thirst, exhaustion, happiness
    :type feelings: list
    """
    def __init__(self, datetime, translation, rotation, color_image,
                 depth_image, feelings):
        """
        Constructor method
        """
        self.datetime = datetime
        self.translation = translation
        self.rotation = rotation
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings

    def __repr__(self):
        return f'Snapshot(datetime={self.datetime})'

    def serialize(self, fields):
        """
        Returns a serialized snapshot with bson.
        
        :param fields: Fields to serialize
        :type fields: list
        :return: A serialized snapshot
        :rtype: bson
        """
        d = self.__dict__.copy()
        for field in d:
            if field not in fields:
                d[field] = None
        return bson.encode(d)

    def to_publish(self, path, user_id):
        """
        Returns a serialized snapshot with json to publish on the message queue.
        
        :param path: The path of the raw_data
        :type path: str
        :param user_id: The id of the user
        :type user_id: int
        :return: A serialized snapshot
        :rtype: json
        """
        d = self.__dict__.copy()
        d['color_image'][2] = str(path / 'color_image')
        d['depth_image'][2] = str(path / 'depth_image.npy')
        d['user_id'] = user_id
        return json.dumps(d)

    @staticmethod
    def deserialize(data):
        """
        Deserialize a snapshot with bson.
        
        :param data: The data to deserialize
        :type data: bson
        :return: The snapshot object
        :rtype: :class:`sphere.protocol.Snapshot`
        """
        return Snapshot(**bson.decode(data))
