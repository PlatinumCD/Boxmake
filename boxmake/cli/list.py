import click

import boxmake
from boxmake.database.edit import read_all_entries

# ==============
# List Command
# ==============

@click.command()
def list():
    print()
    click.secho('Boxmake images:', fg='green')

    print('=' * 20)    
    entries = read_all_entries()
    for entry in entries:
        name, os, packages, date = entry
        print('\t{} ({}): - {}'.format(name, os, date))
        if packages:
            for package in packages.split(' '):
                print('\t\t+ {}'.format(package))
        else:
            print('\t\tNo spack packages or spack installed')
        print()
