#!/usr/bin/env python3

import unittest
import authService.non_persistent_auth

PATH = 'test.db'

class NonPersistentAuthImplementation(unittest.TestCase):

    def test_creation(self):
        '''Test instantiation'''
        auth = authService.non_persistent_auth.NonPersistentAuth()
        self.assertTrue(len(auth.users)== 0)

    def test_create_token(self):
        '''Test create token'''
        USERNAME = "prueba"
        auth = authService.non_persistent_auth.NonPersistentAuth()
        token = auth.create_token(USERNAME)
        self.assertTrue(token in auth.users[USERNAME].values())
        auth.delete_token(token)

    def test_is_valid(self):
        '''Test is valid'''
        USERNAME = "prueba1"
        auth = authService.non_persistent_auth.NonPersistentAuth()
        token = auth.create_token(USERNAME)
        self.assertTrue(auth.is_valid(USERNAME, token))
        self.assertFalse(auth.is_valid(USERNAME, 'wrong-token'))
        auth.delete_token(token)
    
    def test_get_user(self):
        '''Test get user'''
        USERNAME = "prueba2"
        auth = authService.non_persistent_auth.NonPersistentAuth()
        token = auth.create_token(USERNAME)
        self.assertEqual(auth.get_user(token), USERNAME)
        auth.delete_token(token)
    
    def test_incrementa_edad(self):
        '''Test incrementa edad'''
        USERNAME = "prueba3"
        auth = authService.non_persistent_auth.NonPersistentAuth()
        token = auth.create_token(USERNAME)
        edad_1 = auth.users[USERNAME]["edad"]
        auth.incrementa_edad(token)
        edad_2 = auth.users[USERNAME]["edad"]
        self.assertEqual(edad_1, edad_2-1)
        auth.delete_token(token)
    
    def test_delete_token(self):
        USERNAME = "prueba4"
        auth = authService.non_persistent_auth.NonPersistentAuth()
        token = auth.create_token(USERNAME)
        self.assertTrue(auth.is_valid(USERNAME, token))
        auth.delete_token(token)
        self.assertFalse(auth.is_valid(USERNAME, token))
        auth.delete_token(token)
    
    def test_reset_edad(self):
        USERNAME = "prueba5"
        auth = authService.non_persistent_auth.NonPersistentAuth()
        token = auth.create_token(USERNAME)
        auth.reset_edad(token)
        edad = auth.users[USERNAME]["edad"]
        self.assertEqual(edad, 0)
        auth.delete_token(token)