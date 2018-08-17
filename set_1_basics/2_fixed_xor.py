def string_buffer_xor(buffer1, buffer2):
    s1 = bytes.fromhex(buffer1)
    s2 = bytes.fromhex(buffer2)

    return bytes(b1 ^ b2 for b1, b2 in zip(s1, s2)).hex()

# print(string_buffer_xor('1c0111001f010100061a024b53535009181c', '686974207468652062756c6c277320657965'))

import unittest

class TestSet1Challenge2(unittest.TestCase):
    def test_challenge(self):
        buffer1 = '1c0111001f010100061a024b53535009181c'
        buffer2 = '686974207468652062756c6c277320657965'
        result = string_buffer_xor(buffer1, buffer2)

        expected = '746865206b696420646f6e277420706c6179'
        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()
