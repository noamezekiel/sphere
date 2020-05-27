import traceback
import click
from .gui_server import run_server

@click.group()
def main():
    pass

@main.command('run-server')
@click.option('-h', '--host', default='0.0.0.0', type=str)
@click.option('-p', '--port', default=8080, type=int)
@click.option('-d', '--database', default='mongodb://0.0.0.0:27017/', type=str)
def sphere_run_server(host, port, database):
    try:
        run_server(host, port, database)
    except Exception as e:
        print(f'error in gui\'s run-server: {e}')
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    main(prog_name='sphere')