"""
Sending a message:
    Encrypt your plaintext with encrypt_message
    Your id will serve as your public key
Reading a message
    Use decrypt_message and validate contents
"""

import os
import random
from Crypto.PublicKey import RSA

KEYFILE_NAME = 'key1.pem'


def create_key(name=KEYFILE_NAME):
    '''Generates and writes byte string with object of RSA key object.'''
    key = RSA.generate(1024)
    with open(name, 'w') as f:
        f.write(key.exportKey('PEM'))
    return key


def retrieve_key():
    '''
    Reads an exported key-bytestring from file.
    If the file does not exist, create one.
    Returns an RSA key object.
    '''
    #if not os.path.isfile(KEYFILE_NAME):
    #   return create_key()
    n = random.randint(1, 5)
    with open("key"+str(n)+".pem", 'r') as f:
        key = RSA.importKey(f.read())
        return key


def get_public_bytestring():
    key = retrieve_key()
    return key.publickey().exportKey()


def decrypt_message(message):
    '''Use your own private key to decrypt a message.'''
    key = retrieve_key()
    return key.decrypt(message)


def encrypt_message(key_string, message):
    '''Use the given public key to encrypt a message.'''
    key = RSA.importKey(key_string)
    return key.encrypt(message, 123)
