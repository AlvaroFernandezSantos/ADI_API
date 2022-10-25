import hashlib 
import json
import requests

HEADERS = {'Content-Type': 'application/json'}

class RestAuthError(Exception):
    '''Exception raised for errors in the RestAuth client'''

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f'RestAuthError: {self.message}'


class RestAuthClient:
    '''Library to access to the REST API of rest_auth'''

    def __init__(self, uri, timeout=120):
        '''uri should be the root of the API,
            example: http://
        '''
        self.root = uri
        if not self.root.endswith('/'):
            self.root = f'{self.root}/'
        self.timeout = timeout

    def create_user(self, username):
        '''Send request to create a new user'''
        if not isinstance(username, str):
            raise ValueError('username must be a string')
        req_body = {'username': username}
        result = requests.put(
            f'{self.root}v1/users',
            headers=HEADERS,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        if result.status_code != 200:
            raise RestAuthError(f'Unexpected status code: {result.status_code}')

    
    def delete_user(self, username):
        '''Send request to delete a user'''
        if not isinstance(username, str):
            raise ValueError('username must be a string')
        req_body = {'username': username}
        result = requests.delete(
            f'{self.root}v1/users',
            headers=HEADERS,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        if result.status_code != 200:
            raise RestAuthError(f'Unexpected status code: {result.status_code}')

    
    def login(self, username, password):
        '''Send request to login'''
        if not isinstance(username, str):
            raise ValueError('username must be a string')
        if not isinstance(password, str):
            raise ValueError('password must be a string')
        hash_pass = hashlib.sha256(password.encode('utf-8')).hexdigest()
        req_body = {'username': username, 'hash-pass': hash_pass}
        result = requests.post(
            f'{self.root}v1/login',
            headers=HEADERS,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        if result.status_code != 200:
            raise RestAuthError(f'Unexpected status code: {result.status_code}')
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
            headers=HEADERS,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        if result.status_code != 200:
            raise RestAuthError(f'Unexpected status code: {result.status_code}')
    
    
    def check_exists(self , username):
        '''Send request to check if user exists'''
        if not isinstance(username, str):
            raise ValueError('username must be a string')
        req_body = {'username': username}
        result = requests.post(
            f'{self.root}v1/users/{username}',
            headers=HEADERS,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        if result.status_code != 204:
            raise RestAuthError(f'Unexpected status code: {result.status_code}')

    
    def check_token(self, token):
        '''Send request to check if token is valid'''
        if not isinstance(token, str):
            raise ValueError('token must be a string')
        req_body = {'token': token}
        result = requests.post(
            f'{self.root}v1/token/{token}',
            headers=HEADERS,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        if result.status_code != 200:
            raise RestAuthError(f'Unexpected status code: {result.status_code}')


    def check_admin(self, admin_token):
        '''Send request to check if token is valid'''
        if not isinstance(admin_token, str):
            raise ValueError('admin_token must be a string')
        req_body = {'admin-token': admin_token}
        result = requests.post(
            f'{self.root}v1/admin/{admin_token}',
            headers=HEADERS,
            data=json.dumps(req_body),
            timeout=self.timeout
        )
        if result.status_code != 200:
            raise RestAuthError(f'Unexpected status code: {result.status_code}')