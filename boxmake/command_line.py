import boxmake
import docker
import sys
import click

# ==========
# Home Group
# ==========

home_options = {
  'create':  'Create a new docker image',
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
        for usage_type in ['commands', 'flags']:
            click.echo('  boxmake [{}]'.format(usage_type))

    def format_options(self, ctx, formatter):
        click.echo('Commands:')
        for option, option_desc in home_options.items():
            click.echo('  {:18}{}'.format(option, option_desc))
        click.echo()

@click.group(cls=HomeGroup)
def cli():
    pass

@cli.command()
def license():
    click.echo('License:')

@cli.command()
def version():
    click.echo('Version: 0.0.8')


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
    client = docker.from_env(timeout=600)

    # Specify image to pull
    if ':' in image:
        os, tag = image.split(':')
    else:
        os, tag = image, 'latest'


    # Pull image
    image_obj = client.images.pull(os, tag)


    # Parse OS release
    os_release_dict = {}
    os_release = client.containers.run(image, 'cat /etc/os-release', remove=True)
    os_release_parsed = os_release.decode().replace('\"', '').splitlines()
    for item in os_release_parsed:
        item_name, item_value = item.split('=')
        os_release_dict[item_name] = item_value


    # Parse env
    env_dict = {}
    env_data = client.containers.run(image, 'printenv', remove=True)
    env_parsed = env_data.decode().replace('\"', '').splitlines()
    for item in env_parsed:
        item_name, item_value = item.split('=')
        env_dict[item_name] = item_value

    
    # List of commands to execute
    commands = []
   
 
    # OS packages (Ubuntu)
    if 'ubuntu' in image:
        ubuntu_packages = ' '.join([
            'build-essential', 'ca-certificates', 'coreutils', 'curl',
            'environment-modules', 'gfortran', 'git', 'gpg', 'lsb-release',
            'python3', 'python3-distutils', 'python3-venv', 'unzip', 'zip'
        ])

        commands.append('apt-get update')
        commands.append('apt-get install -y {}'.format(ubuntu_packages))


    # OS packages (Centos)
    if os_release_dict['ID'] == 'centos':
        centos_packages = ' '.join([
            'curl', 'findutils', 'gcc-c++', 'gcc', 'gcc-gfortran', 'git', 
            'gnupg2', 'hostname', 'iproute', 'redhat-lsb-core', 'make', 'patch',
            'python3', 'python3-pip', 'python3-setuptools', 'unzip'
        ])

        if os_release_dict['VERSION'] == '8':
            commands.append('yum -y --disablerepo \'*\' --enablerepo=extras swap centos-linux-repos centos-stream-repos')
            commands.append('yum -y distro-sync')
        
        commands.append('yum update -y')
        commands.append('yum install epel-release -y')
        commands.append('yum --enablerepo epel groupinstall -y "Development Tools"')
        commands.append('yum --enablerepo epel install -y {}'.format(centos_packages))
        commands.append('python3 -m pip install boto3')

    # Spack install
    if spack:
        commands.append('git clone https://github.com/spack/spack.git /spack')
        commands.append('cd /spack && git checkout releases/v0.19')
        commands.append('. /spack/share/spack/setup-env.sh')

        commands.append('echo export PATH={}:/spack/bin >> ~/.bashrc'.format(env_dict['PATH']))

        # Spack packages
        for pack in package:
            commands.append('spack install {}'.format(pack))
        

    # Make environment
    env = {
        'PYTHONUNBUFFERED': '1',
        'DEBIAN_FRONTEND': 'noninteractive',
        'PATH': '{}{}'.format(env_dict['PATH'], ':/spack/bin' if spack else '')
    }


    # Run container
    container = client.containers.run(image, detach=True, tty=True)

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
    container.commit(name)
    container.stop()

