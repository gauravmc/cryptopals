LETTER_FREQS = {
    ' ': 13.00, 'E': 12.70, 'T': 9.06, 'A': 8.17,
    'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33,
    'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03,
    'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93,
    'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15,
    'X': 0.15, 'Q': 0.10, 'Z': 0.07
}

def decrypt_single_xor_cipher(string):
    curr_score, message, key_char = 0, '', 0

    for i in range(0, 256):
        curr_msg = single_char_xor(i, string)
        score = sum(LETTER_FREQS.get(chr(byte), 0) for byte in curr_msg.upper())
        if score > curr_score:
            curr_score, message, key_char = score, curr_msg, i

    result = {
        'score': curr_score,
        'message': message.decode('utf-8', 'ignore'),
        'key': key_char
    }

    return result

def single_char_xor(char, string):
    return bytes(str_b ^ char for str_b in bytes.fromhex(string))

import unittest

class TestSet1Challenge3(unittest.TestCase):
    def test_challenge(self):
        result = decrypt_single_xor_cipher('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')

        self.assertEqual(88, result['key'])
        self.assertEqual("Cooking MC's like a pound of bacon", result['message'])

if __name__ == '__main__':
    unittest.main()
