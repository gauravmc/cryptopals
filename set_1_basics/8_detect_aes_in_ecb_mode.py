import os
import sys
sys.path.append(os.path.abspath(os.path.join('lib')))
import utils

#  Remember that the problem with ECB is that it is stateless and deterministic; the same 16 byte plaintext block will always produce the same 16 byte ciphertext.

def detect_which_aes_is_ecb_mode(ciphertexts):
    key_lenghts = [16, 24, 32]
    distances = []

    for key_length in key_lenghts:
        for ciphertext in ciphertexts:
            distance = utils.avg_hamming_distance_over_chunk_size(ciphertext, key_length)
            distances.append({'distance': distance, 'ciphertext': ciphertext})

    return sorted(distances, key=lambda x: x['distance'])[0]['ciphertext']

import unittest

class TestSet1Challenge8(unittest.TestCase):
    def test_detect_aes_ecb_ecrypted_text(self):
        expected = 'd880619740a8a19b7840a8a31c810a3d08649af70dc06f4fd5d2d69c744cd283e2dd052f6b641dbf9d11b0348542bb5708649af70dc06f4fd5d2d69c744cd2839475c9dfdbc1d46597949d9c7e82bf5a08649af70dc06f4fd5d2d69c744cd28397a93eab8d6aecd566489154789a6b0308649af70dc06f4fd5d2d69c744cd283d403180c98c8f6db1f2a3f9c4040deb0ab51b29933f2c123c58386b06fba186a'

        with open(os.path.dirname(os.path.abspath(__file__)) + '/files/challenge_8.txt') as f:
            hexed_texts = f.readlines()
            ciphertexts = list(map(bytes.fromhex, hexed_texts))
            result = detect_which_aes_is_ecb_mode(ciphertexts).hex()
            self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()
