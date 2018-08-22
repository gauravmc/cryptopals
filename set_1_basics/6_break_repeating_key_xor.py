import os
import base64
import sys
sys.path.append(os.path.abspath(os.path.join('lib')))
import utils
from single_byte_xor_cipher import decrypt_single_xor_cipher
from repeating_key_xor import repeating_key_xor

def decrypt_vigenere_cipher(filepath):
    with open(filepath) as f:
        ciphertext = base64.b64decode(f.read())
        key = key_for_vigenere_cipher(ciphertext)
        return bytes.fromhex(repeating_key_xor(key, ciphertext))

def key_for_vigenere_cipher(ciphertext):
    key_size = key_size_with_lowest_normalized_distance(ciphertext)
    blocks = transpose_ciphertext_blocks_of_size(ciphertext, key_size)
    key_chars = []
    for block in blocks:
        result = decrypt_single_xor_cipher(block.hex())
        key_chars.append(chr(result['key']))

    return ''.join(key_chars)

def transpose_ciphertext_blocks_of_size(ciphertext, key_size):
    blocks = [b''] * key_size

    for chunk in utils.chunks_by_size(ciphertext, key_size):
        for i in range(key_size): blocks[i] += chunk[i:i + 1]

    return blocks

def key_size_with_lowest_normalized_distance(ciphertext):
    distances = []
    for key_size in range(2, 41):
        avg_distance = utils.avg_hamming_distance_over_chunk_size(ciphertext, key_size)
        distances.append({'key_size': key_size, 'avg_distance': avg_distance})

    return sorted(distances, key=lambda x: x['avg_distance'])[0]['key_size']

import unittest

class TestSet1Challenge6(unittest.TestCase):
    CIPHER_FILEPATH = os.path.dirname(os.path.abspath(__file__)) + '/files/challenge_6.txt'

    def test_decrypt_vigenere_cipher(self):
        result = decrypt_vigenere_cipher(self.CIPHER_FILEPATH)
        expected = b"I'm back and I'm ringin' the bell \nA rocki"

        self.assertEqual(expected, result[0:42])

    def test_key_for_vigenere_cipher(self):
        result = key_for_vigenere_cipher(self.__sample_ciphertext())
        expected = 'Terminator X: Bring the noise'

        self.assertEqual(expected, result)

    def test_transpose_ciphertext_blocks_of_size(self):
        cipher_string = "0e3647e8592d35514a081243582536ed3de6734059001e3f535ce6271032"
        ciphertext = base64.b64decode(cipher_string)

        blocks = transpose_ciphertext_blocks_of_size(ciphertext, 2)

        expected = b'\xd1\xfa\xb7\xe7\x9d\x9e\xe1<n\xe7\xb9\xa7\xdd\xba~\xe74\xed\xe7\\\xad\xd7\xf6'
        self.assertEqual(expected, blocks[0])
        expected = b'\xed\xe3\xbc\xdd\xdfu\xad\xd77\xcd\xdf\x9d\xd7\xef4\xdd\xd5\xdf~{\xbbM'
        self.assertEqual(expected, blocks[1])

        cipher_string = "0e3647e8592d35514a081243582536ed3de6734059001e3f535ce6271032"
        ciphertext = base64.b64decode(cipher_string)

        blocks = transpose_ciphertext_blocks_of_size(ciphertext, 4)
        self.assertEqual(b'\xd1\xb7\x9d\xe1n\xb9\xdd~4\xe7\xad\xf6', blocks[0])
        self.assertEqual(b'\xed\xbc\xdf\xad7\xdf\xd74\xd5~\xbb', blocks[1])
        self.assertEqual(b'\xfa\xe7\x9e<\xe7\xa7\xba\xe7\xed\\\xd7', blocks[2])
        self.assertEqual(b'\xe3\xddu\xd7\xcd\x9d\xef\xdd\xdf{M', blocks[3])

    def test_lowest_winning_key_size(self):
        cipher_string = "0e3647e8592d35514a081243582536ed3de6734059001e3f535ce6271032\n"\
                        "334b041de124f73c18011a50e608097ac308ecee501337ec3e100854201d\n"\
                        "40e127f51c10031d0133590b1e490f3514e05a54143d08222c2a4071e351\n"\
                        "45440b171d5c1b21342e021c3a0eee7373215c4024f0eb733cf006e2040c"
        ciphertext = base64.b64decode(cipher_string)

        result = key_size_with_lowest_normalized_distance(ciphertext)
        self.assertEqual(33, result)

        result = key_size_with_lowest_normalized_distance(self.__sample_ciphertext())
        self.assertEqual(29, result)

    def __sample_ciphertext(self):
        with open(self.CIPHER_FILEPATH) as f:
            return base64.b64decode(f.read())

if __name__ == '__main__':
    unittest.main()
