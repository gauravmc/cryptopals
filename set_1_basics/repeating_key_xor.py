import itertools
import unittest

def repeating_key_xor(key, string):
    key = itertools.cycle(key)
    return bytes(b ^ ord(next(key)) for b in string).hex()

class TestSet1Challenge5(unittest.TestCase):
    def test_challenge(self):
        stanza = "Burning 'em, if you ain't quick and nimble\n" \
                 "I go crazy when I hear a cymbal"

        expected = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272" \
                   "a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

        self.assertEqual(expected, repeating_key_xor('ICE', stanza.encode()))

if __name__ == '__main__':
    unittest.main()
