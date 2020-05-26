import click
from furl import furl
from . import run_parser
from .. import mq_drivers 


@click.group()
def main():
    pass

@main.command('parse')
@click.argument('parser_name', type=str)
@click.argument('path', type=str)
def sphere_parse(parser_name, path):
    # color-image --> color_image
    parser_name = parser_name.replace('-', '_')
    with open(path, 'rb') as f:
        data = f.read()
    print(run_parser(parser_name, data))

@main.command('run-parser')
@click.argument('parser_name', type=str)
@click.argument('url',default='rabbitmq://127.0.0.1:5672/' ,type=str)
def sphere_run_parser(parser_name, url):
    f = furl(url)
    mq, mq_host, mq_port = f.scheme, f.host, f.port
    driver = mq_drivers[mq]
    # color-image --> color_image
    parser_name = parser_name.replace('-', '_')
    # what the parser should do on every message
    def on_message(topic, message):
        driver.produce(
            host=mq_host,
            port=mq_port,
            message=run_parser(parser_name, message),
            sector='results',
            sector_type='direct',
            topic=parser_name)
    # the parser consumes from the server
    driver.consume(
        host=mq_host,
        port=mq_port,
        on_message=on_message,
        sector='raw_data',
        sector_type='fanout',
        topics=[parser_name])

if __name__ == '__main__':
    main(prog_name='sphere')
