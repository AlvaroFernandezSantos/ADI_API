#!/usr/bin/env python3

'''Ejemplo de API REST para ADI'''

from setuptools import setup

setup(
    name='rest_auth',
    version='0.1',
    description=__doc__,
    packages=['rest_auth', 'rest_auth_scripts'],
    entry_points={
        'console_scripts': [
            'rest_auth_server=rest_auth_scripts.server:main',
            'rest_auth_client=rest_auth_scripts.client:main'
        ]
    }
)