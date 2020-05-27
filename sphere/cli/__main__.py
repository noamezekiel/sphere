import click
import requests

@click.group()
def main():
    pass

@main.command('get-users')
@click.option('-h', '--host', default='0.0.0.0', type=str)
@click.option('-p', '--port', default=5000, type=int)
def sphere_get_users(host, port):
    resp = requests.get(
        f'http://{host}:{port}/users')
    print(resp.json())

@main.command('get-user')
@click.option('-h', '--host', default='0.0.0.0', type=str)
@click.option('-p', '--port', default=5000, type=int)
@click.argument('user_id', type=int)
def sphere_get_user(host, port, user_id):
    resp = requests.get(
        f'http://{host}:{port}/users/{user_id}')
    print(resp.json())

@main.command('get-snapshots')
@click.option('-h', '--host', default='0.0.0.0', type=str)
@click.option('-p', '--port', default=5000, type=int)
@click.argument('user_id', type=int)
def sphere_get_snapshots(host, port, user_id):
    resp = requests.get(
        f'http://{host}:{port}/users/{user_id}/snapshots')
    print(resp.json())

@main.command('get-snapshot')
@click.option('-h', '--host', default='0.0.0.0', type=str)
@click.option('-p', '--port', default=5000, type=int)
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
def sphere_get_snapshot(host, port, user_id, snapshot_id):
    resp = requests.get(
        f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}')
    print(resp.json())

@main.command('get-result')
@click.option('-h', '--host', default='0.0.0.0', type=str)
@click.option('-p', '--port', default=5000, type=int)
@click.option('-s', '--save', default='', type=str)
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=int)
@click.argument('result', type=str)
def sphere_get_result(host, port, save, user_id, snapshot_id, result):
    resp = requests.get(
        f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}/{result}')
    data = resp.json()
    if not save:
        print(data)
    else:
        with open(save) as f:
            f.write(data)

if __name__ == '__main__':
    main(prog_name='sphere')