import click
from furl import furl
from . import Saver
from .. import mq_drivers
from ..parsers import parsers


@click.group()
def main():
    pass

@main.command('save')
@click.option('-d', '--database', default='mongodb://0.0.0.0:27017/', type=str)
@click.argument('topic', type=str)
@click.argument('path', type=str)
def sphere_save(database, topic, path):
    saver = Saver(database)
    with open(path, 'rb') as f:
        raw_data = f.read()
    saver.save(topic, raw_data)

@main.command('run-saver')
@click.argument('db_url', default='mongodb://0.0.0.0:27017/', type=str)
@click.argument('mq_url', default='rabbitmq://0.0.0.0:5672/', type=str)
def sphere_run_saver(db_url, mq_url):
    saver = Saver(db_url)
    f = furl(mq_url)
    mq, mq_host, mq_port = f.scheme, f.host, f.port
    mq_driver = mq_drivers[mq]
    mq_driver.consume(
        host=mq_host,
        port=mq_port,
        on_message=saver.save,
        sector='results',
        topics=list(parsers.keys()) + ['users'],
        sector_type='direct')

    
if __name__ == '__main__':
    main(prog_name='sphere')
