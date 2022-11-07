#!/usr/bin/env python3

import unittest

import authService.auth

PATH = 'test.db'

class AuthServiceImplementation(unittest.TestCase):

    def test_creation(self):
        '''Test instantiation'''
        auth = authService.auth.Auth(PATH)
        self.assertEqual(auth.path, PATH)

    def test_create_user(self):
        '''Test create user'''
        auth = authService.auth.Auth(PATH)
        self.assertTrue(auth.create_user('user1', 'password'))
        self.assertTrue(auth.exists('user1'))

    def test_delete_user(self):
        '''Test delete user'''
        USER2 = 'user2'
        PASSWORD2 = 'password2'
        auth = authService.auth.Auth(PATH)
        auth.create_user(USER2, PASSWORD2)
        self.assertTrue(auth.exists(USER2))
        auth.delete_user(USER2)
        self.assertFalse(auth.exists(USER2))

    def test_set_password(self):
        '''Test set password'''
        USER3 = 'user3'
        PASSWORD3 = 'password3'
        auth = authService.auth.Auth(PATH)
        auth.create_user(USER3, PASSWORD3)
        self.assertTrue(auth.exists(USER3))
        auth.set_password(USER3, 'password')
        self.assertTrue(auth.check_password(USER3, 'password'))

    def test_check_password(self):
        '''Test check password'''
        USER4 = 'user4'
        PASSWORD4 = 'password4'
        auth = authService.auth.Auth(PATH)
        auth.create_user(USER4, PASSWORD4)
        self.assertTrue(auth.exists(USER4))
        auth.set_password(USER4, 'password')
        self.assertTrue(auth.check_password(USER4, 'password'))
        self.assertFalse(auth.check_password(USER4, 'wrong_password'))

    def test_exists(self):
        '''Test exists'''
        USER5 = 'user5'
        PASSWORD5 = 'password5'
        auth = authService.auth.Auth(PATH)
        auth.create_user(USER5, PASSWORD5)
        self.assertTrue(auth.exists(USER5))

    def test_wipe(self):
        '''Test wipe'''
        USER6 = 'user6'
        PASSWORD6 = 'password6'
        auth = authService.auth.Auth(PATH)
        auth.create_user(USER6, PASSWORD6)
        self.assertTrue(auth.exists(USER6))
        auth.wipe()
        self.assertFalse(auth.exists(USER6))