#!/usr/bin/env python3

'''
    REST access library + client example
'''

from rest_auth.client import RestAuthClient

def main():
    '''Entry point'''
    client = RestAuthClient('http://127.0.0.1:4999/')
    print("Creando usuario 'pepe'")
    client.create_user('pepe')

if __name__ == '__main__':
    main()