import unittest
import os
import errno

from nose.tools import assert_equal

from tsukiji import crypto as cr


def silentremove(filename):
    '''Remove a file. If the file does not exist, stay silent.'''
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise


class CryptoTest(unittest.TestCase):
    '''
    Test crypto functions.

    Since crypto is essentially just a wrapper around the PyCrypto library, we will not test this module extensively.
    '''
    def test_create_key(self):
        silentremove(cr.KEYFILE_NAME)
        cr.create_key()
        assert os.path.isfile(cr.KEYFILE_NAME)

    def test_retrieve_key_does_not_exist_yet(self):
        silentremove(cr.KEYFILE_NAME)
        cr.retrieve_key()
        assert os.path.isfile(cr.KEYFILE_NAME)

    def test_retrieve_key(self):
        cr.retrieve_key()
        assert os.path.isfile(cr.KEYFILE_NAME)

    def test_encrypt_decrypt_message(self):
        message = "Hello, world"
        encrypted_message = cr.encrypt_message(cr.get_public_bytestring(), message)
        decrypted_message = cr.decrypt_message(encrypted_message)
        assert_equal(message, decrypted_message)
