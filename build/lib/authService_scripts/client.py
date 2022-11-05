#!/usr/bin/env python3

'''
    REST access library + client example
'''

from authService.client import AuthService

def main():
    '''Entry point'''
    client = AuthService('http://0.0.0.0:3001/')

if __name__ == '__main__':
    main()