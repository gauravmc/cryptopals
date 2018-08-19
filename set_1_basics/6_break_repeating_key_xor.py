import os
import base64

def break_vigenere(filepath):
    # to be written
    # ciphertext = base64.b64decode(''.join(open(filepath).readlines()))
    # print(average_hamming_distance(ciphertext, 4))

    return False

def average_hamming_distance_for_chunk(ciphertext, chunk_size):
    total_chunks = 0
    distances_of_all_chunks = 0

    for pos in range(0, len(ciphertext), chunk_size):
        chunk1 = ciphertext[pos : pos+chunk_size]
        chunk2 = ciphertext[pos+chunk_size : pos+chunk_size*2]
        if len(chunk2) == 0: continue

        total_chunks += 1
        distances_of_all_chunks += hamming_distance(chunk1, chunk2)

    return int(round(distances_of_all_chunks / total_chunks))

def hamming_distance(bytes1, bytes2):
    distance = 0

    for int1, int2 in zip(bytes1, bytes2):
        bin1, bin2 = '{:016b}'.format(int1), '{:016b}'.format(int2)
        distance += sum(bit1 != bit2 for bit1, bit2 in zip(bin1, bin2))

    return distance

import unittest

class TestSet1Challenge6(unittest.TestCase):
    def test_average_hamming_distance(self):
        filepath = os.path.dirname(os.path.abspath(__file__)) + '/files/challenge_6.txt'
        cipher_file = open(filepath)
        ciphertext = base64.b64decode(''.join(cipher_file.readlines()))

        chunk_size = 4
        self.assertEqual(13, average_hamming_distance_for_chunk(ciphertext, chunk_size))

        chunk_size = 8
        self.assertEqual(26, average_hamming_distance_for_chunk(ciphertext, chunk_size))

        cipher_file.close()

    def test_hamming_distance(self):
        distance = hamming_distance(
            'this is a test'.encode(),
            'wokka wokka!!!'.encode()
        )
        expected_distance = 37

        self.assertEqual(expected_distance, distance)

if __name__ == '__main__':
    unittest.main()
