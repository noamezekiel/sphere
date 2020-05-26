import json

def parse_feelings(raw_data):
    data = json.loads(raw_data)
    return json.dumps({'user_id': data['user_id'],
                        'datetime': data['datetime'], 
                        'feelings': data['feelings']})

parse_feelings.fields = {'feelings'}
