import os
import sys
sys.path.append(os.path.abspath(os.path.join('lib')))
import utils

#  Remember that the problem with ECB is that it is stateless and deterministic; the same 16 byte plaintext block will always produce the same 16 byte ciphertext.

def detect_which_aes_is_ecb_mode(ciphertexts):
    key_lenghts = [16, 24, 32] # Possible AES key lenghts
    distances = []

    for key_length in key_lenghts:
        for ciphertext in ciphertexts:
            distance = utils.avg_hamming_distance_over_chunk_size(ciphertext, key_length)
            distances.append({'distance': distance, 'ciphertext': ciphertext})

    return sorted(distances, key=lambda x: x['distance'])[0]['ciphertext']

import unittest

class TestSet1Challenge8(unittest.TestCase):
    def test_detect_aes_ecb_ecrypted_text(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + '/files/challenge_8.txt') as f:
            hexed_texts = list(map(str.strip, f.readlines()))
            ciphertexts = list(map(bytes.fromhex, hexed_texts))

            result = detect_which_aes_is_ecb_mode(ciphertexts).hex()
            expected_text = 'd880619740a8a19b7840a8a31c810a3d08649af70d'
            self.assertEqual(expected_text, result[0:42])

            line_num = hexed_texts.index(result) + 1
            expected_line_num = 133
            self.assertEqual(expected_line_num, line_num)

if __name__ == '__main__':
    unittest.main()
