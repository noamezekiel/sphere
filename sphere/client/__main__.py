import click
from . import upload_sample

@click.group()
def main():
    pass


@main.command('upload-sample')
@click.option('-h', '--host', default='127.0.0.1', type=str)
@click.option('-p', '--port', default=8000, type=int)
@click.argument('path', default='etc/sample.mind.gz')
@click.argument('file_format', default='protobuf')
def sphere_upload_sample(host, port, path, file_format):
    upload_sample(host, port, path, file_format)

if __name__ == '__main__':
    main(prog_name='sphere')
