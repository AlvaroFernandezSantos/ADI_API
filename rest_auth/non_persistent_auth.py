import sqlite3
import uuid

'''
Implementación de la clase de datos no persistentes de autenticación
'''

class NonPersistentAuth:
    ''' Implementa todas las operaciones sobre un objeto tipo NonPersistentAuth() '''

    def __init__(self, AUTH):
        self.users = {}
        self.auth = AUTH

    
    def create_token(self, username, password):
        ''' Crea un nuevo usuario '''
        if self.auth.login(username, password):
            self.users[username] = password
            new_token = uuid.uuid4()
            self.users.update({username: new_token})
            return new_token

    
    def is_valid(self, username, token):
        ''' Comprueba si un token es válido '''
        return self.users.get(username) == token

    
    def get_user(self, token):
        ''' Devuelve el usuario asociado a un token '''
        for user, token in self.users.items():
            if token == token:
                return user


    # Añadir que el token tenga tiempo de caducidad
            