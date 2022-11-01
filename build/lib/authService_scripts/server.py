#!/usr/bin/env python3

'''
    Lanzamiento del servidor de autenticación AuthService
'''

import argparse
from flask import Flask

from authService.server import routeApp
from authService.auth import Auth
from authService.non_persistent_auth import NonPersistentAuth
from os import getcwd

def main():
    '''Entry point'''
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-a', '--admin', type=str, default='admin', help='Token de administrador')
    parser.add_argument('-p', '--port', type=int, default=3001, help='Puerto del servidor')
    parser.add_argument('-l', '--listening', type=str, default='0.0.0.0', help='Direccion del servidor')
    parser.add_argument('-d', '--db', type=str, default=f'{getcwd()}/test.db', help='Ruta a la base de datos')
    args = parser.parse_args()

    print(args.admin)

    np_auth = NonPersistentAuth()

    app = Flask("authService")
    routeApp(app, Auth(args.db), np_auth, args.admin)
    app.run(host=args.listening, port=args.port, debug=True)


if __name__ == '__main__':
    main()