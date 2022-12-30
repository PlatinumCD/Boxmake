from setuptools import setup

setup(
    name='boxmake',
    description='Build docker containers quickly with Spack integration.',
    version='0.0.6',
    install_requires=[
        'docker',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'boxmake = boxmake.command_line:cli',
        ]
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
