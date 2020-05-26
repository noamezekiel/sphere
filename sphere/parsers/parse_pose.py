import json

def parse_pose(raw_data):
    data = json.loads(raw_data)
    result = {'translation': data['translation'], 'rotation': data['rotation']}
    return json.dumps({'user_id': data['user_id'],
                        'datetime': data['datetime'], 
                        'pose': result})

parse_pose.fields = {'translation', 'rotation'}
