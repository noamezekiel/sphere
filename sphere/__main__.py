import os
import sys
import traceback

import click

import brain


class Log:

    def __init__(self):
        self.quiet = False
        self.traceback = False

    def __call__(self, message):
        if self.quiet:
            return
        if self.traceback and sys.exc_info():  # there's an active exception
            message += os.linesep + traceback.format_exc().strip()
        click.echo(message)


log = Log()


@click.group()
@click.version_option(brain.version)
@click.option('-q', '--quiet', is_flag=True)
@click.option('-t', '--traceback', is_flag=True)
def main(quiet=False, traceback=False):
    log.quiet = quiet
    log.traceback = traceback


@main.command('upload_thought')
@click.argument('address', required=True,)
@click.argument('user_id', required=True, type=int)
@click.argument('thought', required=True)
def upload_thought(address, user_id, thought):
    '''Sends to ADDRESS by USER_ID a THOUGHT

    The ADDRESS should be in the form ip_address:port
    '''
    address = (address.split(':')[0], int(address.split(':')[1]))
    log(brain.upload_thought(address, user_id, thought))


@main.command('run_server')
@click.argument('address', required=True)
@click.argument('data_dir', required=True)
def run_server(address, data_dir):
    '''Runs a server at ADDRESS and stores the thoughts in DATA_DIR

    The ADDRESS should be in the form ip_address:port
    '''
    address = (address.split(':')[0], int(address.split(':')[1]))
    log(brain.run_server(address, data_dir))


@main.command('run_webserver')
@click.argument('address', required=True)
@click.argument('data_dir', required=True)
def run_webserver(address, data_dir):
    '''Runs a web server at ADDRESS and servs the thoughts from DATA_DIR

    The ADDRESS should be in the form ip_address:port
    '''
    address = (address.split(':')[0], int(address.split(':')[1]))
    log(brain.run_webserver(address, data_dir))


if __name__ == '__main__':
    try:
        main(prog_name='python -m brain', obj={})
    except Exception as error:
        log(f'ERROR: {error}')
        sys.exit(1)
