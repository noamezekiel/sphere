import json

def parse_pose(raw_data):
    """ Returns a json with the result.
    :param raw_data: The raw_data as consumed from the message queue
    :type raw_data: json
    :return: json dumps of a dictionary with the keys: 'user_id', 'datetime', 'pose'
    :rtype: json 
    """
    data = json.loads(raw_data)
    result = {'translation': data['translation'], 'rotation': data['rotation']}
    return json.dumps({'user_id': data['user_id'],
                        'datetime': data['datetime'], 
                        'pose': result})

parse_pose.fields = {'translation', 'rotation'}
