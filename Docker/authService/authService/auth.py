#!/usr/bin/env python3

''' Implementación de la persistencia del servicio de autenticación'''

import sqlite3

class Auth:
    '''Implementa todas las operaciones sobre un objeto tipo Auth()'''

    def __init__(self, path):
        self.path = path
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS "users" ("username" TEXT, "password" TEXT)')
        conn.commit()

    def get_db_conn(self):
        ''' Retorna la conexión a la bbdd'''
        return sqlite3.connect(self.path)


    def create_user(self, username, password):
        '''Crea un nuevo usuario'''
        db_conn = self.get_db_conn()
        cursor = db_conn.cursor()
        sentence = 'INSERT INTO users VALUES (?, ?)'
        cursor.execute(sentence, (username, password))
        db_conn.commit()
        db_conn.close()
        return True


    def delete_user(self, username):
        '''Elimina un usuario'''
        db_conn = self.get_db_conn()
        cursor = db_conn.cursor()
        sentence = 'DELETE FROM users WHERE username = ?'
        cursor.execute(sentence, (username,))
        db_conn.commit()
        db_conn.close()


    def set_password(self, username, password):
        '''Establece la contraseña de un usuario'''
        db_conn = self.get_db_conn()
        cursor = db_conn.cursor()
        sentence = 'UPDATE users SET password = ? WHERE username = ?'
        cursor.execute(sentence, (password, username))
        db_conn.commit()
        db_conn.close()


    def check_password(self, username, password):
        '''Comprueba la contraseña de un usuario'''
        db_conn = self.get_db_conn()
        cursor = db_conn.cursor()
        sentence = 'SELECT password FROM users WHERE username=?'
        cursor.execute(sentence, (username,))
        possible_password = cursor.fetchone()[0]
        db_conn.close()
        return possible_password == password


    def exists(self, username):
        '''Comprueba si un usuario existe'''
        db_conn = self.get_db_conn()
        sentence = 'SELECT * FROM users WHERE username=?'
        cursor = db_conn.cursor()
        cursor.execute(sentence, (username,))
        possible_user = cursor.fetchone()
        db_conn.close()
        return possible_user is not None


    def wipe(self):
        '''Elimina todos los usuarios'''
        db_conn = self.get_db_conn()
        cursor = db_conn.cursor()
        cursor.execute('DELETE FROM users')
        db_conn.commit()
        db_conn.close()
