import os
import base64

def avg_hamming_distance_for_chunk(ciphertext, chunk_size):
    total_chunks = 0
    distances_of_all_chunks = 0

    previous_chunk, previously_processed_chunk = b'', b''
    for chunk in chunks_by_size(ciphertext, chunk_size):
        total_chunks += 1

        if previous_chunk != previously_processed_chunk:
            distances_of_all_chunks += hamming_distance(previous_chunk, chunk)
            previously_processed_chunk = chunk

        previous_chunk = chunk

    return int(round(distances_of_all_chunks / total_chunks))

def hamming_distance(bytes1, bytes2):
    distance = 0

    for int1, int2 in zip(bytes1, bytes2):
        bin1, bin2 = '{:016b}'.format(int1), '{:016b}'.format(int2)
        distance += sum(bit1 != bit2 for bit1, bit2 in zip(bin1, bin2))

    return distance

def chunks_by_size(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

import unittest

class TestSet1Challenge6(unittest.TestCase):
    def test_average_hamming_distance(self):
        cipher_string = "0e3647e8592d35514a081243582536ed3de6734059001e3f535ce6271032\n"\
                        "334b041de124f73c18011a50e608097ac308ecee501337ec3e100854201d\n"\
                        "40e127f51c10031d0133590b1e490f3514e05a54143d08222c2a4071e351\n"\
                        "45440b171d5c1b21342e021c3a0eee7373215c4024f0eb733cf006e2040c"

        ciphertext = base64.b64decode(cipher_string)
        chunk_size = 4
        self.assertEqual(8, avg_hamming_distance_for_chunk(ciphertext, chunk_size))

        cipher_file = open(os.path.dirname(os.path.abspath(__file__)) + '/files/challenge_6.txt')
        ciphertext = base64.b64decode(''.join(cipher_file.readlines()))

        chunk_size = 4
        self.assertEqual(6, avg_hamming_distance_for_chunk(ciphertext, chunk_size))
        chunk_size = 8
        self.assertEqual(13, avg_hamming_distance_for_chunk(ciphertext, chunk_size))

        cipher_file.close()

    def test_hamming_distance(self):
        distance = hamming_distance(
            'this is a test'.encode(),
            'wokka wokka!!!'.encode()
        )
        expected_distance = 37

        self.assertEqual(expected_distance, distance)

    def test_chunks_by_size(self):
        original_sequence = [1,2,3,4,5,6,7,8]
        result = []
        for chunk in chunks_by_size(original_sequence, 2):
            result.append(chunk[0])
            result.append(chunk[1])

        self.assertEqual(original_sequence, result)

        byte_sequence = b'\x1dB\x1fM\x0b\x0f\x02\x1fO\x13N<\x1aie\x1fI\x1c\x0eN'
        result = b''
        for chunk in chunks_by_size(byte_sequence, 3):
            result += chunk[0:1]
            result += chunk[1:2]
            result += chunk[2:3]

        self.assertEqual(byte_sequence, result)

if __name__ == '__main__':
    unittest.main()
