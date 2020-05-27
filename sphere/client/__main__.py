import traceback
import click
from . import upload_sample

@click.group()
def main():
    pass


@main.command('upload-sample')
@click.option('-h', '--host', default='0.0.0.0', type=str)
@click.option('-p', '--port', default=8000, type=int)
@click.argument('path', default='etc/sample.mind.gz')
@click.argument('file_format', default='protobuf')
def sphere_upload_sample(host, port, path, file_format):
    try:
    	upload_sample(host, port, path, file_format)
    except Exception as e:
        print(f'error in upload_sample: {e}')
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    main(prog_name='sphere')
