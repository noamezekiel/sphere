import traceback
import click
from furl import furl
from .server import run_server
from .. import mq_drivers


@click.group()
def main():
    pass

@main.command('run-server')
@click.option('-h', '--host', default='0.0.0.0', type=str)
@click.option('-p', '--port', default=8000, type=int)
@click.argument('url', default='rabbitmq://0.0.0.0:5672/', type=str)
def sphere_run_server(host, port, url):
    try:
        f = furl(url)
        mq, mq_host, mq_port = f.scheme, f.host, f.port
        driver = mq_drivers[mq]
        # what the server should do on every message
        def publish(message):
            user, snapshot = message
            driver.produce(
                host=mq_host,
                port=mq_port,
                message=snapshot,
                sector='raw_data',
                sector_type='fanout')
            driver.produce(
                host=mq_host,
                port=mq_port,
                message=user,
                sector='results',
                sector_type='direct',
                topic='users')
        run_server(host, port, publish)
    except Exception as e:
        print(f'error in run-server: {e}')
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    main(prog_name='sphere')
