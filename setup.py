from setuptools import setup

setup(
    name='conex',
    version='0.0.1',
    install_requires=[
        'docker',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'conex = conex.command_line:cli',
        ]
    }
)
