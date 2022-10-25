#!/usr/bin/env python3

'''
    Implementacion ejemplo de servidor y servicio auth REST
'''

from flask import Flask

from rest_auth.server import routeApp
from rest_auth.auth import Auth

PATH = 'test.db'

def main():
    '''Entry point'''
    app = Flask("rest_auth")
    routeApp(app, Auth(PATH))
    app.run(debug=True)


if __name__ == '__main__':
    main()