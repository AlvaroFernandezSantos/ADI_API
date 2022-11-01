#!/usr/bin/env python3
import sqlite3

'''
Implementación de servicio de autenticación
'''

class Auth:
    '''Implementa todas las operaciones sobre un objeto tipo Auth()'''

    def __init__(self, path):
        self.path = path
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS "users" ("username" TEXT, "password" TEXT)')
        self.conn.commit()

    def get_db(self):
        ''' Retorna la conexión a la bbdd'''
        return sqlite3.connect(self.path, check_same_thread=False)

    def get_cursor(self):
        '''Retorna el cursor de la base de datos'''
        return self.get_db().cursor()

    def create_user(self, username, password):
        '''Crea un nuevo usuario'''
        db = self.get_db()
        cursor = db.cursor()
        cursor.execute(f'INSERT INTO users VALUES ("{username}", "{password}")')
        db.commit()

    
    def delete_user(self, username):
        '''Elimina un usuario'''
        db = self.get_db()
        cursor = self.get_cursor()
        cursor.execute(f'DELETE FROM users WHERE username="{username}"')
        db.commit()


    def set_password(self, username, password):
        '''Establece la contraseña de un usuario'''
        db = self.get_db()
        cursor = self.get_cursor()
        cursor.execute(f'UPDATE users SET password="{password}" WHERE username="{username}"')
        db.commit()

    
    def check_password(self, username, password):
        '''Comprueba la contraseña de un usuario'''
        cursor = self.get_cursor()
        cursor.execute(f'SELECT password FROM users WHERE username = "{username}"')
        return cursor.fetchone()[0] == password


    def exists(self, username):
        '''Comprueba si un usuario existe'''
        cursor = self.get_cursor()
        cursor.execute(f'SELECT username FROM users WHERE username = "{username}"')
        return cursor.fetchone() is not None


    def wipe(self): # Añadida, arreglar
        '''Elimina todos los usuarios'''
        self.cursor.execute('DELETE FROM users')