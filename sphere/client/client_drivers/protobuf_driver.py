import base64
import gzip
import struct
from google.protobuf.json_format import MessageToDict
from sphere.protocol import User, Snapshot
from . import sphere_pb2  # the protocol between the sample to the client


class Driver():
    """ The protobuf Driver for Reader.
    :param path: The path to the sample
    :type path: str
    """ 
    def __init__(self, path):
        """Constructor method."""
        self.path = path
        self.user = sphere_pb2.User()
        with gzip.open(path, 'rb') as f:
            size, = struct.unpack('I', f.read(4))
            self.user.ParseFromString(f.read(size))
            self._cur = f.tell()

    def __repr__(self, path):
        return f'protobuf Driver(path={self.path})'

    def get_user(self):
        """ Returns the user of the sample.
        :return: The user of the sample
        :rtype: :class:`sphere.protocol.User` object
        """
        user_dict = MessageToDict(
            self.user,
            use_integers_for_enums=True,
            preserving_proto_field_name=True,
            including_default_value_fields=True
        )
        # MessageToDict converts uint64 to string
        # https://github.com/protocolbuffers/protobuf/issues/1823
        user_dict['user_id'] = int(user_dict['user_id'])
        if user_dict['gender'] == 0:
            user_dict['gender'] = 'm'
        elif user_dict['gender'] == 1:
            user_dict['gender'] = 'f'
        else:
            user_dict['gender'] = 'o'
        return User(**user_dict)

    def snapshots(self):
        """ An iterator that iterates over the snapshots."""
        pb_snapshot = sphere_pb2.Snapshot()
        with gzip.open(self.path, 'rb') as f:
            f.seek(self._cur)
            size = f.read(4)
            while size:
                size, = struct.unpack('<I', size)
                pb_snapshot.ParseFromString(f.read(size))
                snapshot = pb_to_snapshot(pb_snapshot)
                yield snapshot
                size = f.read(4)


def pb_to_snapshot(pb_snapshot):
    """ Converts a Snapshot from protobuf object to protocol object.
    :param pb_snaphot: The protobuf snapshot.
    :type pb_snapshot: :class:`sphere_pb2.Snapshot` object
    :return: The snapshot
    :rtype: :class:`sphere.protocol.Snapshot` object
    """
    snapshot_dict = MessageToDict(
            pb_snapshot,
            preserving_proto_field_name=True,
            including_default_value_fields=True
        )
    # for some reason google's MessageToDict converts bytes to base64 string
    # https://github.com/protocolbuffers/protobuf/issues/4525
    snapshot_dict['color_image']['data'] = base64.b64decode(
        snapshot_dict['color_image']['data']
    )
    for key, value in snapshot_dict.items():
        if key == 'pose':
            translation = list(value['translation'].values())
            rotation = list(value['rotation'].values())
        elif key == 'color_image':
            snapshot_dict[key] = list(value.values())
        elif key == 'depth_image':
            snapshot_dict[key] = list(value.values())
        elif key == 'feelings':
            snapshot_dict[key] = list(value.values())
        elif key == 'datetime':
            # MessageToDict converts uint64 to string
            # https://github.com/protocolbuffers/protobuf/issues/1823
            snapshot_dict['datetime'] = int(snapshot_dict['datetime'])
        else:
            snapshot_dict[key] = value
    del snapshot_dict['pose']
    snapshot_dict['translation'] = translation
    snapshot_dict['rotation'] = rotation
    return Snapshot(**snapshot_dict)
