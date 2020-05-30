import json
import pathlib
from PIL import Image as PIL
from utils import DIRECTORY

def parse_color_image(raw_data):
    """
    Returns a json with a path to the color image.
    
    :param raw_data: The raw_data as consumed from the message queue
    :type raw_data: json
    :return: json dumps of a dictionary with the keys: 'user_id', 'datetime', 'color_image'
    :rtype: json 
    """
    directory = pathlib.Path(DIRECTORY) / 'results'
    data = json.loads(raw_data)
    path = directory / \
            str(data['user_id']) / \
            str(data['datetime']) / \
            'color_image.jpg'
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
    # data['color_image'] = (width, height, path/to/bytes)
    size = data['color_image'][:2]
    with open(data['color_image'][2], 'rb') as f:
        image = PIL.frombytes('RGB', size, f.read())
    image.save(path)
    return json.dumps({'user_id': data['user_id'],
                        'datetime': data['datetime'], 
                        'color_image': str(path)})

parse_color_image.fields = {'color_image'}