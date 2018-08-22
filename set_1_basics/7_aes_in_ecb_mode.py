import os
import base64
from Crypto.Cipher import AES

def decrypt_aes_ecb_cipher(key, ciphertext):
    return AES.new(key, AES.MODE_ECB).decrypt(ciphertext).decode()

import unittest

class TestSet1Challenge7(unittest.TestCase):
    CIPHER_FILEPATH = os.path.dirname(os.path.abspath(__file__)) + '/files/challenge_7.txt'

    def test_decryption_of_aes_ecb_input(self):
        with open(self.CIPHER_FILEPATH) as f:
            ciphertext = base64.b64decode(f.read())
            key = 'YELLOW SUBMARINE'
            result = decrypt_aes_ecb_cipher(key, ciphertext)
            self.assertEqual("I'm back and I'm ringin' the bell \nA rocki", result[0:42])

if __name__ == '__main__':
    unittest.main()
