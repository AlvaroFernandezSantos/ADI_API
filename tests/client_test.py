#!/usr/bin/env python3

import unittest
import authService.client
import authService.auth

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

class UserImplementation(unittest.TestCase):

    def test_creation(self):
        '''Test instantiation'''
        user = authService.client.User(URL, 'user1', 'token')
        self.assertEqual(user.url, URL)

    def test_set_password(self):
        '''Test set password'''
        USER3 = 'user3'
        PASSWORD3 = 'password3'
        user = authService.client.User(URL, USER3, 'token')
        auth = authService.auth.Auth(PATH)
        admin = authService.client.Administrator(URL, TOKEN)
        admin.new_user(USER3, PASSWORD3)
        self.assertTrue(auth.exists(USER3))
        # El usuario necesita hacer login para conseguir su token -> Sino no tiene permiso para cambiarse la contraseña
        user.set_new_password('password')
        self.assertTrue(auth.check_password(USER3, 'password'))

class AuthServiceImplementation(unittest.TestCase):

    def test_creation(self):
        '''Test instantiation'''
        auth = authService.client.AuthService(URL)
        self.assertEqual(auth.uri, URL)

    def test_user_of_token(self):
        '''Test user of token'''
        USER4 = 'user4'
        PASSWORD4 = 'password4'
        auth = authService.client.AuthService(URL)
        admin = authService.client.Administrator(URL, TOKEN)
        admin.new_user(USER4, PASSWORD4)
        token = auth.login(USER4, PASSWORD4)
        self.assertEqual(auth.user_of_token(token), USER4)

    def test_exists_user(self):
        '''Test exists user'''
        USER5 = 'user5'
        PASSWORD5 = 'password5'
        auth = authService.client.AuthService(URL)
        admin = authService.client.Administrator(URL, TOKEN)
        admin.new_user(USER5, PASSWORD5)
        self.assertTrue(auth.exists_user(USER5))

    def test_admin_login(self):
        '''Test admin login'''
        # Por hacer
    
    def test_user_login(self):
        '''Test user login'''
        USER7 = 'user7'
        PASSWORD7 = 'password7'
        auth = authService.client.AuthService(URL)
        admin = authService.client.Administrator(URL, TOKEN)
        admin.new_user(USER7, PASSWORD7)
        user = auth.user_login(USER7, PASSWORD7)
        self.assertTrue(user.username == USER7 and user.token != None)

