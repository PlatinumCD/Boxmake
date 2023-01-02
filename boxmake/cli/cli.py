import sys
import click
from .create import create
from .add import add
from .list import list

# ==========
# Home Group
# ==========

home_options = {
  'create':  'Create a new docker image',
  'delete':  'Delete a boxmake image [NOT IMPLEMENTED]',
  'list':    'List boxmake images [NOT IMPLEMENTED]',
  'add':     'Add spack packages to a docker image [NOT IMPLEMENTED]',
  'remove':  'Remove spack packages to a docker image [NOT IMPLEMENTED]',
  'version': 'The current version of the boxmake runtime'
}

class HomeGroup(click.Group):
    def format_help(self, ctx, formatter):
        click.echo('Python Version: {}'.format(sys.version))
        click.echo()
        click.echo('\tboxmake is the CLI for interacting with docker images and spack packages', nl=False)
        click.echo()
        click.echo()
        self.format_usage(ctx, formatter)
        click.echo()
        self.format_options(ctx, formatter)

    def format_usage(self, ctx, formatter):
        click.echo('Usage:')
        click.echo('  boxmake [commands]')

    def format_options(self, ctx, formatter):
        click.echo('Commands:')
        for option, option_desc in home_options.items():
            click.echo('  {:18}{}'.format(option, option_desc))

@click.group(cls=HomeGroup)
def entry():
    pass

@entry.command()
def license():
    click.echo('License:')

@entry.command()
def version():
    click.echo('Version: 0.0.11')

entry.add_command(create)
entry.add_command(add)
entry.add_command(list)
