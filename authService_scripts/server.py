#!/usr/bin/env python3

''' Lanzamiento del servidor de autenticación AuthService '''

import uuid
import argparse

from os import getcwd
from flask import Flask
from authService.server import routeApp
from authService.auth import Auth
from authService.non_persistent_auth import NonPersistentAuth

def main():
    '''Entry point'''
    token = str(uuid.uuid4())
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-a', '--admin', type=str, default=token, help='Token de administrador')
    parser.add_argument('-p', '--port', type=int, default=3001, help='Puerto del servidor')
    parser.add_argument('-l', '--listening', type=str, default='0.0.0.0', help='Direccion del servidor')
    parser.add_argument('-d', '--db', type=str, default=f'{getcwd()}', help='Ruta a la base de datos')
    args = parser.parse_args()

    print(f'Admin token: {args.admin}')

    np_auth = NonPersistentAuth()

    app = Flask("authService")
    routeApp(app, Auth(args.db), np_auth, args.admin)
    app.run(host=args.listening, port=args.port, debug=False)


if __name__ == '__main__':
    main()
