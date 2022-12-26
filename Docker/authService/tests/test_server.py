import unittest
import requests
import json

HEADERS = {'Content-Type': 'application/json'}
ADMIN_HEADERS = {'Content-Type': 'application/json', 'admin-token': 'admin'}
URL = "http://172.17.0.2:3001/"

class AuthServerImplementation(unittest.TestCase):

    def test_creation(self):
        '''Test instantiation'''
        result = requests.get(f'{URL}v1/user/admin',headers=ADMIN_HEADERS, timeout=120)
        self.assertEqual(result.status_code, 204)

    def test_login(self):
        correct_content = {'user': 'prueba', 'hash-pass': 'prueba'}
        wrong_content = {'user': 'asdasdas', 'hash-pass': 'asdasdasdads'}
        no_user_content = {'hash-pass': 'prueba'}
        no_pass_content = {'user': 'prueba'}

        # Insertar usuario
        result = requests.put(f'{URL}v1/user/prueba',headers=ADMIN_HEADERS, data=json.dumps(no_user_content), timeout=120)
        self.assertEqual(result.status_code, 200)
        result = requests.post(f'{URL}v1/user/login',headers=HEADERS, data=json.dumps(correct_content), timeout=120)
        self.assertEqual(result.status_code, 200)
        result = requests.post(f'{URL}v1/user/login',headers=HEADERS, data=json.dumps(no_user_content), timeout=120)
        self.assertEqual(result.status_code, 400)
        result = requests.post(f'{URL}v1/user/login',headers=HEADERS, data=json.dumps(no_pass_content), timeout=120)
        self.assertEqual(result.status_code, 400)
        result = requests.post(f'{URL}v1/user/login',headers=HEADERS, data=json.dumps(wrong_content), timeout=120)
        self.assertEqual(result.status_code, 400)
        result = requests.post(f'{URL}v1/user/login',headers=HEADERS, timeout=120)
        self.assertEqual(result.status_code, 400)
        result = requests.delete(f'{URL}v1/user/prueba',headers=ADMIN_HEADERS, data=json.dumps(correct_content), timeout=120)
        self.assertEqual(result.status_code, 204)

    def test_create_user(self):
        USER2 = 'prueba2'
        correct_content = {'user': USER2, 'hash-pass': 'prueba'}
        wrong_content = {'user': 'admin', 'hash-pass': 'asuidyasd'}
        no_user_content = {'hash-pass': 'prueba'}
        no_pass_content = {'user': USER2}

        # Insertar usuario
        result = requests.put(f'{URL}v1/user/{USER2}',headers=ADMIN_HEADERS, data=json.dumps(no_user_content), timeout=120)
        self.assertEqual(result.status_code, 200)
        result = requests.put(f'{URL}v1/user/{USER2}',headers=ADMIN_HEADERS, data=json.dumps(wrong_content), timeout=120)
        self.assertEqual(result.status_code, 400)
        result = requests.put(f'{URL}v1/user/{USER2}',headers=ADMIN_HEADERS, data=json.dumps(no_user_content), timeout=120)
        self.assertEqual(result.status_code, 400)
        result = requests.put(f'{URL}v1/user/{USER2}',headers=ADMIN_HEADERS, data=json.dumps(no_pass_content), timeout=120)
        self.assertEqual(result.status_code, 400)
        result = requests.put(f'{URL}v1/user/{USER2}',headers=HEADERS, data=json.dumps(no_pass_content), timeout=120)
        self.assertEqual(result.status_code, 401)
        result = requests.put(f'{URL}v1/user/{USER2}',timeout=120)
        self.assertEqual(result.status_code, 400)
        result = requests.delete(f'{URL}v1/user/{USER2}',headers=ADMIN_HEADERS, data=json.dumps(correct_content), timeout=120)
        self.assertEqual(result.status_code, 204)

    def test_change_password(self):
        USER3 = 'prueba3'
        user_content = {'user': USER3, 'hash-pass': 'prueba'}
        no_user_content = {'hash-pass': 'prueba'}
        no_pass_content = {'user': USER3}

        # Insertar usuario
        result = requests.put(f'{URL}v1/user/{USER3}',headers=ADMIN_HEADERS, data=json.dumps(user_content), timeout=120)
        self.assertEqual(result.status_code, 200)
        # Login para obtener token
        result = requests.post(f'{URL}v1/user/login',headers=HEADERS, data=json.dumps(user_content), timeout=120)
        self.assertEqual(result.status_code, 200)
        new_token = json.loads(result.content.decode())['token']
        new_headers = {'Content-Type': 'application/json', 'user-token': new_token}

        # Cambiar contraseña
        result = requests.post(f'{URL}v1/user/{USER3}', timeout=120)
        self.assertEqual(result.status_code, 400)
        result = requests.post(f'{URL}v1/user/{USER3}',headers=HEADERS, data=json.dumps(no_user_content), timeout=120)
        self.assertEqual(result.status_code, 401)
        result = requests.post(f'{URL}v1/user/{USER3}',headers=new_headers, data=json.dumps(no_pass_content), timeout=120)
        self.assertEqual(result.status_code, 400)
        result = requests.post(f'{URL}v1/user/{USER3}',headers=new_headers, data=json.dumps(user_content), timeout=120)
        self.assertEqual(result.status_code, 200)
        result = requests.delete(f'{URL}v1/user/{USER3}',headers=ADMIN_HEADERS, timeout=120)
        self.assertEqual(result.status_code, 204)

    def test_user_exists(self):
        USER4 = 'prueba4'
        correct_content = {'user': 'USER4', 'hash-pass': 'prueba'}
        no_user_content = {'hash-pass': 'prueba'}

        # Insertar usuario
        result = requests.put(f'{URL}v1/user/{USER4}',headers=ADMIN_HEADERS, data=json.dumps(correct_content), timeout=120)
        self.assertEqual(result.status_code, 200)
        result = requests.get(f'{URL}v1/user/{USER4}',headers=HEADERS, data=json.dumps(correct_content), timeout=120)
        self.assertEqual(result.status_code, 204)
        result = requests.get(f'{URL}v1/user/prueba98765',headers=HEADERS, data=json.dumps(no_user_content), timeout=120)
        self.assertEqual(result.status_code, 404)
        result = requests.delete(f'{URL}v1/user/{USER4}',headers=ADMIN_HEADERS, data=json.dumps(correct_content), timeout=120)
        self.assertEqual(result.status_code, 204)

    def test_delete_user(self):
        USER5 = 'prueba5'
        correct_content = {'user': USER5, 'hash-pass': 'prueba'}

        # Insertar usuario
        result = requests.put(f'{URL}v1/user/{USER5}',headers=ADMIN_HEADERS, data=json.dumps(correct_content), timeout=120)
        self.assertEqual(result.status_code, 200)

        # Borrar usuario
        result = requests.delete(f'{URL}v1/user/{USER5}',headers=HEADERS, data=json.dumps(correct_content), timeout=120)
        self.assertEqual(result.status_code, 401)
        result = requests.delete(f'{URL}v1/user/pruebaisydasd',headers=ADMIN_HEADERS, data=json.dumps(correct_content), timeout=120)
        self.assertEqual(result.status_code, 404)

        result = requests.delete(f'{URL}v1/user/{USER5}',headers=ADMIN_HEADERS, data=json.dumps(correct_content), timeout=120)
        self.assertEqual(result.status_code, 204)

    def test_token_exists(self):
        USER6 = 'prueba6'
        correct_content = {'user': USER6, 'hash-pass': 'prueba'}

        # Insertar usuario
        result = requests.put(f'{URL}v1/user/{USER6}',headers=ADMIN_HEADERS, data=json.dumps(correct_content), timeout=120)
        self.assertEqual(result.status_code, 200)
        # Login para obtener token
        result = requests.post(f'{URL}v1/user/login',headers=HEADERS, data=json.dumps(correct_content), timeout=120)
        self.assertEqual(result.status_code, 200)
        new_token = json.loads(result.content.decode())["token"]
        # Comprobar token
        result = requests.get(f'{URL}v1/token/{new_token}',headers=HEADERS, timeout=120)
        self.assertEqual(result.status_code, 200)
        result = requests.get(f'{URL}v1/token/dfsajasdflkj',headers=HEADERS, data=json.dumps(correct_content), timeout=120)
        self.assertEqual(result.status_code, 404)
        # Eliminar usuario
        result = requests.delete(f'{URL}v1/user/{USER6}',headers=ADMIN_HEADERS, data=json.dumps(correct_content), timeout=120)
        self.assertEqual(result.status_code, 204)
    
    def test_admin_exists(self):

        # Comprobar token de administrador
        result = requests.get(f'{URL}v1/user/admin',headers=ADMIN_HEADERS, timeout=120)
        self.assertEqual(result.status_code, 204)
        result = requests.get(f'{URL}v1/user/admin',headers=HEADERS, timeout=120)
        self.assertEqual(result.status_code, 401)
