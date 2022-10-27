#!/usr/bin/env python3

import json
from flask import make_response, request

def routeApp(app, AUTH, tokens, admin_token):
    ''' Enruta la API REST a la webapp '''

    @app.route('/v1/user/login', methods=['POST'])
    def login():
        ''' Login de usuario '''
        if not request.is_json:
            return make_response('Missing JSON', 400)
        if 'user' not in request.get_json():
            return make_response('Missing "user" key', 400)
        if 'hash-pass' not in request.get_json():
            return make_response('Missing "hash-pass" key', 400)
        username = request.get_json()['username']
        password = request.get_json()['password']
        if not AUTH.exists(username):
            return make_response('User does not exist', 400)
        new_token = tokens.create_token(username, password)
        respuesta = {"user": username, "token": new_token}
        return make_response(json.dumps(respuesta), 200)


    @app.route('/v1/user/<username>', methods=['PUT'])
    def create_user(username):
        ''' Crear un nuevo usuario '''
        if not request.headers.get('admin-token') or request.headers.get('admin-token') != admin_token:
            return make_response('Missing admin-token', 401)

        if not request.is_json:
            return make_response('Missing JSON', 400)
        if 'hash-pass' not in request.get_json():
            return make_response('Missing "hash-pass" key', 400)
        password = request.get_json()['password']
        AUTH.create_user(username, password)
        response = {"user": username}
        return make_response(json.dumps(response), 200)


    @app.route('/v1/user/<username>', methods=['POST'])
    def change_password(username):
        ''' Cambiar contraseña de un usuario '''
        if not request.headers.get('admin-token') or request.headers.get('admin-token') != admin_token:
            return make_response('Missing admin-token', 401)

        if not request.is_json:
            return make_response('Missing JSON', 400)
        if 'hash-pass' not in request.get_json():
            return make_response('Missing "hash-pass" key', 400)
        password = request.get_json()['password']
        AUTH.change_password(username, password)
        response = {"user": username}
        return make_response(json.dumps(response), 200)

    
    @app.route('/v1/user/<username>', methods=['GET'])
    def exists(username):
        ''' Comprobar si un usuario existe '''
        if AUTH.exists(username):
            return make_response("", 204)
        return make_response("User not found", 404)


    @app.route('/v1/user/<username>', methods=['DELETE'])
    def delete_user(username):
        ''' Borrar un usuario '''
        if not request.headers.get('admin-token') or request.headers.get('admin-token') != admin_token:
            return make_response('Missing admin-token', 401)

        if not AUTH.exists(username):
            return make_response("User not found", 404)

        AUTH.delete_user(username)
        return make_response("", 204)

    
    @app.route('/v1/token/token', methods=['GET'])
    def token_exists(token):
        ''' Comprobar si un token existe '''            
        if tokens.exists(token):
            response = {"user": tokens.get_user(token)}
            return make_response(json.dumps(response), 200)
        return make_response("Token not found", 404) 

    
    @app.route('/v1/user/admin', methods=['GET'])
    def admin_exists():
        ''' Comprobar si existe el usuario admin '''
        if request.headers.get("admin-token") == admin_token:
            return make_response("", 204)
        return make_response("", 401)