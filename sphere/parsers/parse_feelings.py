import json

def parse_feelings(raw_data):
    """
    Returns a json with the result.
    
    :param raw_data: The raw_data as consumed from the message queue
    :type raw_data: json
    :return: json dumps of a dictionary with the keys: 'user_id', 'datetime', 'feelings'
    :rtype: json 
    """
    data = json.loads(raw_data)
    return json.dumps({'user_id': data['user_id'],
                        'datetime': data['datetime'], 
                        'feelings': data['feelings']})

parse_feelings.fields = {'feelings'}
