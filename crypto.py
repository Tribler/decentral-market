"""
Sending a message:
    Encrypt your plaintext with encrypt_message
    Your id will serve as your public key
Reading a message
    Use decrypt_message and validate contents
"""

from Crypto.PublicKey import RSA


# Generates and writes byte string with object of RSA key object
def create_key():
    key = RSA.generate(2048)
    f = open('key.pem', 'w')
    f.write(key.exportKey('PEM'))
    f.close()


# Reads an exported key-bytestring from file and returns an RSA key object
def retrieve_key():
    f = open('key.pem', 'r')
    key = RSA.importKey(f.read())
    return key


def get_public_bytestring():
    key = retrieve_key()
    return key.publickey().exportKey()


# Use own private key to decrypt broadcasted message
def decrypt_message(message):
    key_obj = retrieve_key()
    return key_obj.decrypt(message)


# Use given id to encrypt message
def encrypt_message(key_string, message):
    key = RSA.importKey(key_string)
    return key.encrypt(message, 123)