#!/usr/bin/env python3
import sqlite3

'''
Implementación de servicio de autenticación
'''

class Auth:
    '''Implementa todas las operaciones sobre un objeto tipo Auth()'''

    def __init__(self, path):
        self.path = path
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS "users" ("username" TEXT, "password" TEXT)')
        conn.commit()

    def get_db(self):
        ''' Retorna la conexión a la bbdd'''
        return sqlite3.connect(self.path)


    def create_user(self, username, password):
        '''Crea un nuevo usuario'''
        db = self.get_db()
        cursor = db.cursor()
        cursor.execute(f'INSERT INTO users VALUES ("{username}", "{password}")')
        db.commit()
        db.close()
        return True

    
    def delete_user(self, username):
        '''Elimina un usuario'''
        db = self.get_db()
        cursor = db.cursor()
        sentence = 'DELETE FROM users WHERE username = ?'
        cursor.execute(sentence, (username,))
        db.commit()
        db.close()


    def set_password(self, username, password):
        '''Establece la contraseña de un usuario'''
        db = self.get_db()
        cursor = db.cursor()
        sentence = 'UPDATE users SET password = ? WHERE username = ?'
        cursor.execute(sentence, (password, username))
        db.commit()
        db.close()

    
    def check_password(self, username, password):
        '''Comprueba la contraseña de un usuario'''
        db = self.get_db()
        cursor = db.cursor()
        sentence = 'SELECT password FROM users WHERE username=?'
        cursor.execute(sentence, (username,))
        possible_password = cursor.fetchone()[0]
        db.close()
        return possible_password == password


    def exists(self, username):
        '''Comprueba si un usuario existe'''
        db = self.get_db()
        sentence = 'SELECT * FROM users WHERE username=?'
        cursor = db.cursor()
        cursor.execute(sentence, (username,))
        possible_user = cursor.fetchone()
        db.close()
        return possible_user is not None


    def wipe(self):
        '''Elimina todos los usuarios'''
        db = self.get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM users')
        db.commit()
        db.close()
