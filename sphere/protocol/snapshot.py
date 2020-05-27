import bson
import json
import pathlib


class Snapshot():
    def __init__(self, datetime, translation, rotation, color_image,
                 depth_image, feelings):
        self.datetime = datetime
        self.translation = translation
        self.rotation = rotation
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings

    def __repr__(self):
        return f'Snapshot(datetime={self.datetime})'

    def serialize(self, fields):
        d = self.__dict__.copy()
        for field in d:
            if field not in fields:
                d[field] = None
        return bson.encode(d)

    def to_publish(self, path, user_id):
        d = self.__dict__.copy()
        d['color_image'][2] = str(path / 'color_image')
        d['depth_image'][2] = str(path / 'depth_image.npy')
        d['user_id'] = user_id
        return json.dumps(d)

    @staticmethod
    def deserialize(data):
        return Snapshot(**bson.decode(data))
