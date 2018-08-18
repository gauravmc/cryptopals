def something():
    return True

def hamming_distance(string1, string2):
    distance = 0

    for int1, int2 in zip(string1.encode(), string2.encode()):
        bin1, bin2 = '{:016b}'.format(int1), '{:016b}'.format(int2)
        distance += sum(bit1 != bit2 for bit1, bit2 in zip(bin1, bin2))

    return distance

import unittest

class TestSet1Challenge6(unittest.TestCase):
    def test_challenge(self):
        self.assertTrue(something())

    def test_hamming_distance(self):
        distance = hamming_distance('this is a test', 'wokka wokka!!!')
        expected_distance = 37

        self.assertEqual(expected_distance, distance)

if __name__ == '__main__':
    unittest.main()
