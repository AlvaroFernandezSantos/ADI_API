#!/usr/bin/env python3

'''Ejemplo de API REST para ADI'''

from setuptools import setup

setup(
    name='authService',
    version='0.1',
    description=__doc__,
    packages=['authService', 'authService_scripts'],
    entry_points={
        'console_scripts': [
            'authService_server=authService_scripts.server:main',
            'authService_client=authService_scripts.client:main'
        ]
    }
)