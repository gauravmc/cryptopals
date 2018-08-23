import unittest
from pkcs_7_padding import add_pkcs_padding
import sys, os
sys.path.append(os.path.abspath(os.path.join('lib')))
import utils
import base64
from Crypto.Cipher import AES

AES_KEY_LENGTHS = [16, 24, 32]

def encrypt_with_aes_cbc_mode(key, plaintext):
    key = key.encode()
    if len(key) not in AES_KEY_LENGTHS: raise Exception("Invalid key length, must be either 16, 24, or 32.")
    block_size = len(key)

    if (len(plaintext) % block_size != 0):
        expected_size = len(plaintext) + (block_size - len(plaintext) % block_size)
        plaintext = add_pkcs_padding(plaintext, expected_size)

    iv = chr(0).encode() * block_size

    previous_cipher_block = iv
    ecb = AES.new(key, AES.MODE_ECB)
    ciphertext = b''
    for block in utils.chunks_by_size(plaintext, block_size):
        xored_block = bytes(b1 ^ b2 for b1, b2 in zip(block, previous_cipher_block))
        encrypted_block = ecb.encrypt(xored_block)
        previous_cipher_block = encrypted_block
        ciphertext += encrypted_block

    return ciphertext

class TestSet2Challenge10(unittest.TestCase):
    def test_encrypt_with_aes_cbc_mode(self):
        key = "YELLOW SUBMARINE"
        plaintext = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam eleifend porta odio"\
                " sed rhoncus. Maecenas sed condimentum ligula, ut scelerisque magna. Pellentesque"\
                " posuere dolor id venenatis porta. Duis eget aliquet tortor. Suspendisse at est velit."\
                " Ut tortor felis, dignissim sed maximus ac, dictum eget nulla. Lorem ipsum dolor sit"\
                " amet, consectetur adipiscing elit. Sed sit amet dolor erat.".encode()

        result = encrypt_with_aes_cbc_mode(key, plaintext)
        result = base64.b64encode(result)

        expected = b'6tzFqkgA3/F1pJzzoPIEHdhSL3ANKH1G/v4SUQ1ibypgJvD8Y2wyDZCUjQE7T8AsM9leXD6e+uRxgNgEm'\
                b'XqeuGTQPZfGQR5KWC2FH46kBKLGwz49PmVYVj/6FenwIkXhZUbOc405LgLlJ/etKNUXV89gplJjyJukpX3'\
                b'6YnPfnyCq5vyUzn9i0DiQbFskzNjG9DqUNTTZD1kAMI6CWtOyOwBii1BtTurIqMnKO42f4k/j3b5c5LtkL'\
                b'hw8dBn8W/aUrLHrU9iu0LfW7UtOo/w+xG02mi6GRyFLnAxScOCS9w2XIEJ8dFAWSD9mE4PGHjkB1/o4pq8'\
                b't4H3Ok1LpcSEb0uwYQR4pdt5SdIz0AR6JP0gLWaDvrEFBlDPgdGS4lEnsQJ+fxmTFP/TgFgArIDM7AMFhw'\
                b'+Qbs5/3rl+OT/QDVtqxi0YqUNeHkF7NVkhGHT+KPiySythnchkGSErdRyxV1k4rfHaS6xKuNdfFTS7BwlB'\
                b'Wu76VEaCzVlwv2SlnnYNA0AMqAUHFytZ4LmeJhfBaBw=='

        self.assertEqual(expected, result)

    def test_assert_invalid_key_length(self):
        with self.assertRaises(Exception) as cm:
            encrypt_with_aes_cbc_mode("INVALID KEY", "encrypt me".encode())

        self.assertEqual("Invalid key length, must be either 16, 24, or 32.", str(cm.exception))

if __name__ == '__main__':
    unittest.main()
