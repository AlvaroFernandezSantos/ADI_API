import hashlib 
import json
import requests

class AuthServiceError(Exception):
    '''Exception raised for errors in the AuthService client'''

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'AuthServiceError: {self.message}'


class Administrator:
    ''' Cliente de autenticación como administrador'''

    def __init__(self, url, token):
        self.url = url
        self.__token = token
        self.__headers = {'Content-Type': 'application/json', 'admin-token': self.__token}

    @property
    def headers(self):
        ''' Retorna los headers del administrador '''
        return self.__headers
    
    def new_user(self, username, password):
        ''' Crea un nuevo usuario'''
        if not isinstance(username, str):
            raise ValueError('Username must be a string')
        if not isinstance(password, str):
            raise ValueError('Password must be a string')
        req_body = {'user': username, "hash-pass": password}
        result = requests.put(
            f'{self.url}v1/user',
            headers=self.headers,
            data=json.dumps(req_body),
            timeout=self.timeout)
        if result.status_code != 200:
            raise AuthServiceError(f'Unexpected status code: {result.status_code}')

    def remove_user(self, username):
        if not isinstance(username, str):
            raise ValueError('Username must be a string')
        req_body = {'username': username}
        result = requests.delete(
            f'{self.url}v1/user',
            headers=self.headers,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        if result.status_code != 200:
            raise AuthServiceError(f'Unexpected status code: {result.status_code}')    


class User:
    '''  Cliente de autenticación como usuario '''

    def __init__(self, url,  username, token):
        self.url = url
        self.__username = username
        self.__token = token
        self.__headers = {'Content-Type': 'application/json', 'user-token': self.__token}

    @property
    def headers(self):
        ''' Retorna los headers del usuario '''
        return self.__headers
    
    @property
    def token(self):
        ''' Retorna el token del usuario '''
        return self.__token

    def set_new_password(self, new_password):
        ''' Cambia la contraseña del usuario '''
        if not isinstance(new_password, str):
            raise ValueError('Password must be a string')
        req_body = {'hash-pass': new_password}
        result = requests.post(
            f'{self.url}v1/user/{self.username}',
            headers=self.headers,
            data=json.dumps(req_body),
            timeout=self.timeout)
        if result.status_code != 200:
            raise AuthServiceError(f'Unexpected status code: {result.status_code}')


class AuthService:
    '''Cliente de acceso al servicio de autenticacion'''

    def __init__(self, uri, timeout=120):
        '''uri should be the root of the API,
            example: http://
        '''
        self.root = uri
        if not self.root.endswith('/'):
            self.root = f'{self.root}/'
        self.timeout = timeout

        self.headers = {'Content-Type': 'application/json'}


    def user_of_token(self, token):
        '''Return username of the given token or error'''


    def exists_user(self, username):
        '''Return if given user exists or not'''
        if not isinstance(username, str):
            raise ValueError('Username must be a string')
        req_body = {'user': username}
        result = requests.post(
            f'{self.root}v1/user',
            headers=self.headers,
            data=json.dumps(req_body),
            timeout=self.timeout)
        if result.status_code != 204:
            raise AuthServiceError(f'Unexpected status code: {result.status_code}')
        return result.content.decode('utf-8') == 'true' # Comprobar esto

    def administrator_login(self, token):
        '''Return Adminitrator() object or error'''
        raise NotImplementedError()

    def user_login(self, username, password):
        '''Return User() object or error'''
        if not isinstance(username, str):
            raise ValueError('Username must be a string')
        if not isinstance(password, str):
            raise ValueError('Password must be a string')
        hash_pass = hashlib.sha256(password.encode('utf-8')).hexdigest()
        req_body = {'user': username, 'hash-pass': hash_pass}
        result = requests.post(
            f'{self.root}v1/user/login',
            headers=self.headers,
            data=json.dumps(req_body),
            timeout=self.timeout)
        if result.status_code != 200:
            raise AuthServiceError(f'Unexpected status code: {result.status_code}')
        # Construir el objeto User
        return User(username, result.content.decode('utf-8'))



    
    def user_login(self, username, password):
        '''Send request to login'''
        if not isinstance(username, str):
            raise ValueError('username must be a string')
        if not isinstance(password, str):
            raise ValueError('password must be a string')
        hash_pass = hashlib.sha256(password.encode('utf-8')).hexdigest()
        req_body = {'username': username, 'hash-pass': hash_pass}
        result = requests.post(
            f'{self.root}v1/login',
            headers=self.headers,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        if result.status_code != 200:
            raise AuthServiceError(f'Unexpected status code: {result.status_code}')
        return result.content.decode('utf-8')

    
    def change_password(self, username, password):
        '''Send request to change password'''
        if not isinstance(username, str):
            raise ValueError('username must be a string')
        if not isinstance(password, str):
            raise ValueError('password must be a string')
        hash_pass = hashlib.sha256(password.encode('utf-8')).hexdigest()
        req_body = {'username': username, 'hash-pass': hash_pass}
        result = requests.post(
            f'{self.root}v1/change-password',
            headers=self.headers,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        if result.status_code != 200:
            raise AuthServiceError(f'Unexpected status code: {result.status_code}')
    
    
    def check_exists(self , username):
        '''Send request to check if user exists'''
        if not isinstance(username, str):
            raise ValueError('username must be a string')
        req_body = {'username': username}
        result = requests.post(
            f'{self.root}v1/user/{username}',
            headers=self.headers,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        if result.status_code != 204:
            raise AuthServiceError(f'Unexpected status code: {result.status_code}')

    
    def check_token(self, token):
        '''Send request to check if token is valid'''
        if not isinstance(token, str):
            raise ValueError('token must be a string')
        req_body = {'token': token}
        result = requests.post(
            f'{self.root}v1/token/{token}',
            headers=self.headers,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        if result.status_code != 200:
            raise AuthServiceError(f'Unexpected status code: {result.status_code}')


    def check_admin(self, admin_token):
        '''Send request to check if token is valid'''
        if not isinstance(admin_token, str):
            raise ValueError('admin_token must be a string')
        req_body = {'admin-token': admin_token}
        result = requests.post(
            f'{self.root}v1/admin/{admin_token}',
            headers=self.headers,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        if result.status_code != 200:
            raise AuthServiceError(f'Unexpected status code: {result.status_code}')