import sys, os
sys.path.append(os.path.abspath(os.path.join('lib')))
import utils
import pkcs_7_padding
from Crypto.Cipher import AES

AES_KEY_LENGTHS = [16, 24, 32]

def encrypt_with_aes_cbc_mode(key, plaintext, iv = None):
    key = key.encode()
    if len(key) not in AES_KEY_LENGTHS: raise Exception("Invalid key length, must be either 16, 24, or 32.")

    block_size = len(key)
    plaintext = pkcs_7_padding.add_pkcs_padding_by_block_size(plaintext, block_size)
    if iv is None: iv = chr(0).encode() * block_size

    previous_cipher_block = iv
    ecb = AES.new(key, AES.MODE_ECB)
    ciphertext = b''
    for block in utils.chunks_by_size(plaintext, block_size):
        xored_block = bytes(b1 ^ b2 for b1, b2 in zip(block, previous_cipher_block))
        encrypted_block = ecb.encrypt(xored_block)
        previous_cipher_block = encrypted_block
        ciphertext += encrypted_block

    return ciphertext

def decrypt_aes_cbc_mode_cipher(key, ciphertext, iv):
    key = key.encode()
    if len(key) not in AES_KEY_LENGTHS: raise Exception("Invalid key length, must be either 16, 24, or 32.")

    previous_block = iv
    ecb = AES.new(key, AES.MODE_ECB)
    plaintext = b''
    for block in utils.chunks_by_size(ciphertext, len(key)):
        decrypted_block = ecb.decrypt(block)
        plaintext_block = bytes(b1 ^ b2 for b1, b2 in zip(decrypted_block, previous_block))
        previous_block = block
        plaintext += plaintext_block

    return plaintext

import unittest
import base64

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

    def test_encrypt_with_aes_cbc_mode_with_optional_iv(self):
        key = "THE ANSWER IS 42"
        iv = chr(10).encode() * len(key)
        plaintext = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam eleifend porta odio"\
                " sed rhoncus. Maecenas sed condimentum ligula, ut scelerisque magna.".encode()

        result = encrypt_with_aes_cbc_mode(key, plaintext, iv)
        result = base64.b64encode(result)

        expected = b'KCBXWIMIGsFiq9Y/kFInid+awsKAtH3hajZ0Fl9bfQ+1DwZiECFmWn5M41kVMJqx8PlsDT+bIhA'\
                b'ghOYcrMkd8fatNVu8y3G2J4ebY7W2g05hc9hDycIq0sdjVSMaUHBamRe0ewFPBEA03qYvbG4IkZh'\
                b'+Bq/P4kYKoAImYSBoe0FTzoLt93Pjn+3OGq8FRiMl6qxu0zh8qrFk+wAAYJC+tw=='
        self.assertEqual(expected, result)

    def test_decrypt_aes_cbc_mode_cipher(self):
        key = "THE ANSWER IS 42"
        iv = chr(0).encode() * len(key)
        cipher = b'NBo4N27GikuJ8L2iJUOVNykAOBEMVTptg9Bg/JHCwZSkB77elJh/RkPcFbCIyZhR5+gyCO14aYwJzHya'\
                b'HyM353gS2sKOhKqBnZE/Kmyxlphc/wozbEuXZPy7KZDPv1oL5QiQVynqPwTGLTmTppYxnP+EY7kAzah'\
                b'GoWubUatyaf8i1OlZwRGWCqRS8GHJZ9j12EfK7zkwBVLM/0q4FWf8A8kvDfkr9gfTOZPXE22pIQlxHF'\
                b'Z8MNaSihm/H6m+2DIrK77SVIPLFJrRWc1rFs9vMYxKYmBBSArWpJMaD7bYU+/DhBNnz/4xYU6sf8a0h'\
                b'NV69CibOHDWZcTnavTxbBSndRPi6c0EpSJtFxTeVDJ9Z0e+gbcFPJoAwCQScjppbVJOZXVXrDGzw77g'\
                b'XKs3J8K/zEsAf+1Gx6IfPaudwagmEGCclqCUaVVXlC9BQaLSz7GoBwumuLN8ZWR9iARTR6QCyrmRjtW'\
                b'5OhSQ7mJ90wRyiblkXsPQISxXvfFNPRXVwRM5KJYsP2VGZpuBCWE0StmM9A=='

        ciphertext = base64.b64decode(cipher)

        result = decrypt_aes_cbc_mode_cipher(key, ciphertext, iv)

        expected = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam eleifend porta odio"\
                " sed rhoncus. Maecenas sed condimentum ligula, ut scelerisque magna. Pellentesque"\
                " posuere dolor id venenatis porta. Duis eget aliquet tortor. Suspendisse at est velit."\
                " Ut tortor felis, dignissim sed maximus ac, dictum eget nulla. Lorem ipsum dolor sit"\
                " amet, consectetur adipiscing elit. Sed sit amet dolor erat.\t\t\t\t\t\t\t\t\t".encode()

        self.assertEqual(expected, result)

    def test_decryption_of_given_cbc_cipher_file(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/files/challenge_10.txt') as f:
            ciphertext = base64.b64decode(f.read())
            key = "YELLOW SUBMARINE"
            iv = chr(0).encode() * len(key)

            result = decrypt_aes_cbc_mode_cipher(key, ciphertext, iv)

            expected = "I'm back and I'm ringin' the bell \nA rocki"
            self.assertEqual(expected, result.decode()[0:42])

    def test_assert_invalid_key_length(self):
        with self.assertRaises(Exception) as cm:
            encrypt_with_aes_cbc_mode("INVALID KEY", "encrypt me".encode())

        self.assertEqual("Invalid key length, must be either 16, 24, or 32.", str(cm.exception))

        with self.assertRaises(Exception) as cm:
            decrypt_aes_cbc_mode_cipher("INVALID KEY", "decrypt me".encode(), chr(0).encode())

        self.assertEqual("Invalid key length, must be either 16, 24, or 32.", str(cm.exception))

if __name__ == '__main__':
    unittest.main()
