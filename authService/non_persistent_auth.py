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
        self.timers = {} # {token:timer}
        auth = Auth(f'{getcwd()}/test.db')

    def __del__(self):
        ''' Destructor '''
        for timer in self.timers.values():
            timer.cancel()
            timer.join()

    def create_token(self, username):
        ''' Crea un nuevo token '''
        token = str(uuid.uuid4())
        edad = 0
        self.users[username] = {"token": token, "edad": edad}
        timer = threading.Timer(5, self.incrementa_edad, [token])
        timer.start()
        self.timers.update({token: timer})
        return token


    def is_valid(self, username, token):
        ''' Comprueba si un token es válido '''
        try:
            return self.users[username]["token"] == token
        except KeyError:
            return False


    def get_user(self, token):
        ''' Devuelve el usuario asociado a un token '''
        for user, values in self.users.items():
             if values["token"] == token:
                return user


    def incrementa_edad(self, token):
        ''' Incrementa la edad de un token '''
        current_list = self.users.copy()
        for user, values in current_list.items():
            if values["token"] == token:
                self.users[user]["edad"] += 1
                if self.users[user]["edad"] > 180:
                    self.delete_token(token)
                else:
                    timer = threading.Timer(5, self.incrementa_edad, [token])
                    timer.start()
                    self.timers.update({token: timer})


    def delete_token(self, token):
        ''' Elimina un token '''
        current_list = self.users.copy()
        for user, values in current_list.items():
            if values["token"] == token:
                self.users.pop(user)
                self.timers[token].cancel()
                self.timers[token].join()
                self.timers.pop(token)


    def reset_edad(self, token):
        ''' Reinicia la edad de un token '''
        for user, values in self.users.items():
            if values["token"] == token:
                self.users[user]["edad"] = 0
            