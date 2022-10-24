#!/usr/bin/env python3
import sqlite3

'''
Implementación de servicio de autenticación
'''

class Auth:
    '''Implementa todas las operaciones sobre un objeto tipo Auth()'''

    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
        self.conn.commit()


    def create_user(self, username):
        '''Crea un nuevo usuario'''
        self.cursor.execute(f'INSERT INTO users VALUES ({username}, NULL)')

    
    def delete_user(self, username):
        '''Elimina un usuario'''
        self.cursor.execute(f'DELETE FROM users WHERE username = {username}')

    
    def set_password(self, username, password):
        '''Establece la contraseña de un usuario'''
        self.cursor.execute(f'UPDATE users SET password = {password} WHERE username = {username}')

    
    def check_password(self, username, password):
        '''Comprueba la contraseña de un usuario'''
        self.cursor.execute(f'SELECT password FROM users WHERE username = {username}')
        return self.cursor.fetchone()[0] == password


    def exists(self, username):
        '''Comprueba si un usuario existe'''
        self.cursor.execute(f'SELECT username FROM users WHERE username = {username}')
        return self.cursor.fetchone() is not None


    def wipe(self): # Añadida
        '''Elimina todos los usuarios'''
        self.cursor.execute('DELETE FROM users')