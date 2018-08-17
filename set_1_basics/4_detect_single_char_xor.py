import os
from single_byte_xor_cipher import decrypt_xor_cipher

def detect_xored_string(filepath):
    curr_score, message, line_num = 0, '', 0

    with open(filepath) as f:
        for i, line in enumerate(f):
            result = decrypt_xor_cipher(line.rstrip())
            if result['score'] > curr_score:
                curr_score, line_num = result['score'], i
                message = result['message'].strip()

    return {'line_num': line_num, 'message': message}

import unittest

class TestSet1Challenge4(unittest.TestCase):
    def test_challenge(self):
        result = detect_xored_string(os.path.dirname(os.path.abspath(__file__)) + '/files/challenge_4.txt')

        self.assertEqual(170, result['line_num'])
        self.assertEqual('Now that the party is jumping', result['message'])

if __name__ == '__main__':
    unittest.main()
