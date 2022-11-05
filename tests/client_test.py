#!/usr/bin/env python3

import unittest
import authService.client
import authService.auth
import hashlib

URL = "http://localhost:3001/"
TOKEN = "admin"
PATH = 'test.db'


class AdminImplementation(unittest.TestCase):

    def test_creation(self):
        '''Test instantiation'''
        admin = authService.client.Administrator(URL, TOKEN)
        self.assertEqual(admin.url, URL)
    
    def test_new_user(self):
        '''Test new user'''
        admin = authService.client.Administrator(URL, TOKEN)
        admin.new_user('user1', 'password')
        auth = authService.auth.Auth(PATH)
        self.assertTrue(auth.exists('user1'))
        admin.remove_user('user1')
        self.assertFalse(auth.exists('user1'))
    
    def test_remove_user(self):
        '''Test remove user'''
        USER2 = 'user2'
        PASSWORD2 = 'password2'
        admin = authService.client.Administrator(URL, TOKEN)
        admin.new_user(USER2, PASSWORD2)
        auth = authService.auth.Auth(PATH)
        self.assertTrue(auth.exists(USER2))
        admin.remove_user(USER2)
        self.assertFalse(auth.exists(USER2))

class AuthServiceClientImplementation(unittest.TestCase):

    def test_creation(self):
        '''Test instantiation'''
        auth = authService.client.AuthService(URL)
        self.assertEqual(auth.root, URL)

    def test_user_login(self):
        '''Test user login'''
        USERNAME = "prueba"
        admin = authService.client.Administrator(URL, TOKEN)
        admin.new_user(USERNAME, "password")
        auth = authService.client.AuthService(URL)
        self.assertTrue(auth.exists_user(USERNAME))
        user_result = auth.user_login(USERNAME, "password")
        self.assertEqual(user_result.username, USERNAME)
        admin.remove_user(USERNAME)
        self.assertRaises(authService.client.AuthServiceError, auth.exists_user, USERNAME)


    def test_user_of_token(self):
        '''Test user of token'''
        # Crear usuario
        USERNAME = "prueba25"
        admin = authService.client.Administrator(URL, TOKEN)
        admin.new_user(USERNAME, "password")

        # Hacer login para conseguir token nuevo
        auth = authService.client.AuthService(URL)
        user_result = auth.user_login(USERNAME, "password")

        # Contrastar token
        self.assertEqual(auth.user_of_token(user_result.token), user_result.username)

        # Borrar usuario
        admin.remove_user(USERNAME)
        self.assertRaises(authService.client.AuthServiceError, auth.exists_user, USERNAME)


class UserImplementation(unittest.TestCase):

    def test_creation(self):
        '''Test instantiation'''
        user = authService.client.User(URL, 'user1', 'token')
        self.assertEqual(user.url, URL)

    def test_set_password(self):
        '''Test set password'''
        USER3 = 'user3'
        PASSWORD3 = 'password3'
        auth = authService.auth.Auth(PATH)
        auth_service = authService.client.AuthService(URL)
        admin = authService.client.Administrator(URL, TOKEN)
        # Insertar usuario
        admin.new_user(USER3, PASSWORD3)
        self.assertTrue(auth.exists(USER3))
        
        # Login para obtener token 
        new_user = auth_service.user_login(USER3, PASSWORD3)

        # Cambiar contraseña
        new_user.set_new_password('password')
        hash_pass = hashlib.sha256('password'.encode('utf-8')).hexdigest()
        self.assertTrue(auth.check_password(USER3, hash_pass))

        # Borrar usuario
        admin.remove_user(USER3)
        self.assertFalse(auth.exists(USER3))


class AuthServiceImplementation(unittest.TestCase):

    def test_creation(self):
        '''Test instantiation'''
        auth = authService.client.AuthService(URL)
        self.assertEqual(auth.root, URL)

    def test_exists_user(self):
        '''Test exists user'''
        USER5 = 'user5'
        PASSWORD5 = 'password5'
        auth = authService.client.AuthService(URL)
        admin = authService.client.Administrator(URL, TOKEN)
        admin.new_user(USER5, PASSWORD5)
        self.assertTrue(auth.exists_user(USER5))
        admin.remove_user(USER5)
        self.assertRaises(authService.client.AuthServiceError, auth.exists_user, USER5)


    def test_admin_login(self):
        '''Test admin login'''
        BAD_TOKEN = "bad_token"
        RIGHT_TOKEN = "admin"

        auth = authService.client.AuthService(URL)
        self.assertRaises(authService.client.AuthServiceError, auth.administrator_login, BAD_TOKEN)
        self.assertIsInstance(auth.administrator_login(RIGHT_TOKEN), authService.client.Administrator)
    
    def test_user_login(self):
        '''Test user login'''
        USER7 = 'user7'
        PASSWORD7 = 'password7'
        auth = authService.client.AuthService(URL)
        admin = authService.client.Administrator(URL, TOKEN)
        admin.new_user(USER7, PASSWORD7)
        user = auth.user_login(USER7, PASSWORD7)
        self.assertTrue(user.username == USER7 and user.token != "default")
        admin.remove_user(USER7)
        self.assertRaises(authService.client.AuthServiceError, auth.exists_user, USER7)


