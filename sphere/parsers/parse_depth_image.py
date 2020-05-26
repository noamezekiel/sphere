import json
import numpy as np
import matplotlib.pyplot as plt
import pathlib
from utils import DIRECTORY

def parse_depth_image(raw_data):
    directory = pathlib.Path(DIRECTORY) / 'results'
    data = json.loads(raw_data)
    path = directory / \
            str(data['user_id']) / \
            str(data['datetime']) / \
            'depth_image.jpg'
    if not path.parent.exists():
        path.parent.mkdir(parents=True)
    # data['depth_image'] = (width, height, path/to/bytes)
    image = np.load(data['depth_image'][2])
    image = image.reshape(
                data['depth_image'][1],
                data['depth_image'][0])
    plt.imshow(image)
    plt.savefig(path)
    return json.dumps({'user_id': data['user_id'],
                        'datetime': data['datetime'], 
                        'depth_image': str(path)})

parse_depth_image.fields = {'depth_image'}
