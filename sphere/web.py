from pathlib import Path
from flask import Flask

web_site = Flask('brain')

_INDEX_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface</title>
    </head>
    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''
_USER_LINE_HTML = '''
<li><a href="/users/{user_id}">user {user_id}</a></li>
'''
_USER_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface: User {user_id}</title>
    </head>
    <body>
        <table>
            {data}
        </table>
    </body>
</html>

'''
_DATA_LINE_HTML = '''
<tr>
    <td>{time}</td>
    <td>{data}</td>
</tr>
'''


@web_site.route('/')
def index():
    users_html = []
    for user_dir in data_dir.iterdir():
        users_html.append(_USER_LINE_HTML.format(user_id=user_dir.name))
    index_html = _INDEX_HTML.format(users='\n'.join(users_html))
    return index_html, 200


@web_site.route('/users/<string:user_id>')
def user(user_id):
    data_html = []
    user_dir = data_dir / user_id
    if not user_dir.exists():
        return '', 404

    for data_file in user_dir.iterdir():
        with data_file.open() as f:
            timestamp = data_file.name[:-4].replace('_', '-').rsplit('-')
            time = '-'.join(timestamp[:3]) + ' ' + ':'.join(timestamp[3:])
            data_html.append(_DATA_LINE_HTML.format(time=time,
                                                    data=f.readline()))
    user_html = _USER_HTML.format(user_id=user_id, data='\n'.join(data_html))
    return user_html, 200


def run_webserver(address, data):
    global data_dir
    data_dir = Path(data)
    try:
        web_site.run(*address)
    except KeyboardInterrupt:
        print('')
