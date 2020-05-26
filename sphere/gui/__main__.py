import click
from .gui_server import run_server

@click.group()
def main():
    pass

@main.command('run-server')
@click.option('-h', '--host', default='127.0.0.1', type=str)
@click.option('-p', '--port', default=8080, type=int)
@click.option('-d', '--database', default='mongodb://127.0.0.1:27017/', type=str)
def sphere_run_server(host, port, database):
    run_server(host, port, database)

if __name__ == '__main__':
    main(prog_name='sphere')