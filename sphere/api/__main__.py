import click
from .api_server import run_api_server

@click.group()
def main():
    pass

@main.command('run-server')
@click.option('-h', '--host', default='0.0.0.0', type=str)
@click.option('-p', '--port', default=5000, type=int)
@click.option('-d', '--database', default='mongodb://0.0.0.0:27017/', type=str)
def sphere_run_server(host, port, database):
    run_api_server(host, port, database)

if __name__ == '__main__':
    main(prog_name='sphere')