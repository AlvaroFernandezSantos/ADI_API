import uuid
import threading
from authService.auth import Auth
from os import getcwd

'''
Implementación de la clase de datos no persistentes de autenticación
'''

class NonPersistentAuth:
    ''' Implementa todas las operaciones sobre un objeto tipo NonPersistentAuth() '''

    def __init__(self):
        self.users = {} # {username: {token:token, edad:edad}}
        auth = Auth(f'{getcwd()}/test.db')


    def create_token(self, username, password):
        ''' Crea un nuevo token '''
        if self.auth.exits_user(username, password):
            token = str(uuid.uuid4())
            edad = 0
            self.users[username] = {"token": token, "edad": edad}
            timer = threading.Timer(5, self.incrementa_edad, [token])
            timer.start()
            return token


    def is_valid(self, username, token):
        ''' Comprueba si un token es válido '''
        return self.users[username]["token"] == token


    def get_user(self, token):
        ''' Devuelve el usuario asociado a un token '''
        for user, values in self.users.items():
             if values.get("token") == token:
                return user


    def incrementa_edad(self, token):
        ''' Incrementa la edad de un token '''
        for user, values in self.users.items():
            if values.get("token") == token:
                self.users[user]["edad"] += 1
                if self.users[user]["edad"] > 180:
                    self.delete_token(token)
                else:
                    timer = threading.Timer(5, self.incrementa_edad, [token])
                    timer.start()


    def delete_token(self, token):
        ''' Elimina un token '''
        for user, values in self.users.items():
            if values.get("token") == token:
                self.users.pop(user)


    def reset_edad(self, token):
        ''' Reinicia la edad de un token '''
        for user, values in self.users.items():
            if values.get("token") == token:
                self.users[user]["edad"] = 0
            