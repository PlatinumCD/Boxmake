from setuptools import setup

setup(
    name='binmake',
    description='Build docker containers quickly with Spack integration.',
    version='0.0.1',
    install_requires=[
        'docker',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'binmake = binmake.command_line:cli',
        ]
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
