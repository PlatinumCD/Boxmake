import boxmake
import docker
import sys
import click

# ==========
# Home Group
# ==========

home_options = {
  'create':  'Create a new docker image',
  'list':    'List boxmake images',
  'add':     'Add spack packages to a docker image',
  'remove':  'Remove spack packages to a docker image',
  'version': 'The current version of the boxmake runtime'
}

home_flags = {
  '-h, --help':    'Help for boxmake',
  '-v, --version': 'Display current build version'
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
        for usage_type in ['commands', 'flags']:
            click.echo('  boxmake [{}]'.format(usage_type))

    def format_options(self, ctx, formatter):
        click.echo('Commands:')
        for option, option_desc in home_options.items():
            click.echo('  {:18}{}'.format(option, option_desc))
        click.echo()
        click.echo('Flags:')
        for flag, flag_desc in home_flags.items():
            click.echo('  {:18}{}'.format(flag, flag_desc))

@click.group(cls=HomeGroup)
def cli():
    pass

@cli.command()
def license():
    click.echo('License:')

@cli.command()
def version():
    click.echo("Version: 0.0.3")


# ==============
# Create Command
# ==============

@cli.command()
@click.option('-i', '--image', required=True, help='base image to use')
@click.option('-n', '--name', required=True, help='tag the container')
@click.option('-p', '--package', required=False, help='spack package to include', multiple=True)
@click.option('--spack/--no-spack', help='download spack', default=True)
def create(image, name, package, spack):
    print()
    click.secho('Boxmake', fg='green')
    print('image: ', image)
    print('name: ', name)
    print('packages: ', list(package))
    print('Spack: ', spack)
    print()

    # Get docker client
    client = docker.from_env()


    # Get specified OS
    os, tag = image.split(':')
    image_obj = client.images.pull(os, tag)


    # List of commands to execute
    commands = []

    
    # OS packages (Ubuntu)
    if 'ubuntu' in image:
        ubuntu_packages = ' '.join([
            'build-essential', 'ca-certificates', 'coreutils', 'curl', 'environment-modules', 'gfortran', 'git', 'gpg', 'lsb-release', 'python3', 'python3-distutils', 'python3-venv', 'unzip', 'zip'])

        commands.append('apt-get update')
        commands.append('apt-get install -y {}'.format(ubuntu_packages))


    # OS packages (Centos)
    if 'centos' in image:
        if tag.split('.')[0] == '8':
            commands.append('yum -y --disablerepo \'*\' --enablerepo=extras swap centos-linux-repos centos-stream-repos')
            commands.append('yum -y distro-sync')
        
        commands.append('yum update -y')
        commands.append('yum install epel-release -y')
        commands.append('yum --enablerepo epel groupinstall -y "Development Tools"')
        commands.append('yum --enablerepo epel install -y curl findutils gcc-c++ gcc gcc-gfortran git gnupg2 hostname iproute redhat-lsb-core make patch python3 python3-pip python3-setuptools unzip')
        commands.append('python3 -m pip install boto3')


    # Spack install
    if spack:
        commands.append('git clone https://github.com/spack/spack.git /spack')
        commands.append('cd /spack && git checkout releases/v0.19')
        commands.append('. /spack/share/spack/setup-env.sh')


    # Spack packages
    for pack in package:
        commands.append('./spack/bin/spack install {}'.format(pack))


    # Run container
    env = {
        'PYTHONUNBUFFERED': '1',
    }
    container = client.containers.run(image,  detach=True, tty=True)

    # Run commands
    for command in commands:
        click.secho('=' * 90, color='green')
        print('Command: ', command)
        click.secho('=' * 90, color='green')
        rv, stream = container.exec_run(
            'bash -c \"{}\"'.format(command),
            stream=True,
            environment=env
        )

        print()
        for chunk in stream:
            print(chunk.decode().strip())
        print()


    # Commit new image
    container.stop()
    container.commit(name)

