import requests


def get_config(address, user_id, user_name, user_bd, user_gender):
    user_data = {'user_id': str(user_id), 'user_name': user_name, 'user_bd': str(user_bd), 
                 'user_gender': user_gender}
    r = requests.get(f'https:/{address}/config', params=user_data)


