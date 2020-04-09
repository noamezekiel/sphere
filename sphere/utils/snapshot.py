import datetime as dt
import struct
from PIL import Image


class Snapshot():
    def __init__(self, timestamp, translation, rotation, color_image,
                 depth_image, feelings):
        self.timestamp = timestamp
        self.translation = translation
        self.rotation = rotation
        self.color_image = color_image
        self.depth_image = depth_image
        self.feelings = feelings

    @staticmethod
    def load_snap(path, offset):
        with open(path, 'rb') as f:
            f.seek(offset)
            ts = dt.datetime.fromtimestamp(
                 struct.unpack('Q', f.read(8))[0] / 1000.0)
            translation = struct.unpack('ddd', f.read(24))
            rotation = struct.unpack('dddd', f.read(32))
            # for the color image
            height, width = struct.unpack('II', f.read(8))
            color_image = Image.new('RGB', (width, height))
            data = [[]] * height * width
            for i in range(height * width):
                b, g, r = struct.unpack('BBB', f.read(3))
                data[i] = (r, g, b)
            color_image.putdata(data)
            # for the depth image
            height, width = struct.unpack('II', f.read(8))
            depth_image = Image.new('F', (width, height))
            data = [[]] * height * width
            for i in range(height * width):
                data[i], = struct.unpack('f', f.read(4))
            depth_image.putdata(data)
            feelings = struct.unpack('ffff', f.read(16))
            size = f.tell() - offset
        return Snapshot(ts, translation, rotation, color_image,
                        depth_image, feelings), size
