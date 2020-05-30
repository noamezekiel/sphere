import logging
import requests
from .reader import Reader


def upload_sample(path, host='0.0.0.0', port=8000, file_format='protobuf'):
    logging.basicConfig(level=logging.INFO)
    reader = Reader(path, file_format)
    user = reader.user
    data = user.serialize()
    logging.info(f'sending message from user {user.user_id}')
    logging.debug(f'details:\n{user}')
    resp = requests.get(
        f'http://{host}:{port}/config',
        data=data
    )
    if resp.status_code != 200:
        logging.error('config failed')
        return 1
    fields = resp.json()['fields']
    logging.info(f'fields available- {fields}')
    logging.info(f'sending snapshots from user {user.user_id}')
    for snapshot in reader:
        data = snapshot.serialize(fields)
        logging.info(f'sending snapshot {snapshot.datetime} from user {user.user_id}')
        resp = requests.post(
            f'http://{host}:{port}/snapshot',
            params={'user': user.serialize()},
            data=data
        )
        if resp.status_code != 200:
            logging.error('uploading snapshot failed')
