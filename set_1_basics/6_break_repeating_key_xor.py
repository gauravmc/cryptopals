import os
import base64
from single_byte_xor_cipher import decrypt_xor_cipher

def key_for_vigenere_cipher(filepath):
    cipher_file = open(filepath)
    ciphertext = base64.b64decode(''.join(cipher_file.readlines()))

    key_size = key_size_with_lowest_avg_ham_distance(ciphertext)

    for size in range(key_size, key_size + 3): # Take first 2-3 smallest key sizes
        blocks = transpose_ciphertext_in_blocks_for_size(ciphertext, size)
        for block in blocks:
            print(decrypt_xor_cipher(block.hex())['message'])

    cipher_file.close()
    return 'key'

def transpose_ciphertext_in_blocks_for_size(ciphertext, key_size):
    blocks = [b''] * key_size

    for chunk in chunks_by_size(ciphertext, key_size):
        for i in range(key_size): blocks[i] += chunk[i:i + 1]

    return blocks

def key_size_with_lowest_avg_ham_distance(ciphertext):
    winning_key_size = 0
    lowest_distance = 2**100 # Arbitrary large int

    for key_size in range(2, 41):
        distance = avg_hamming_distance_for_chunk(ciphertext, key_size)
        if distance < lowest_distance:
            lowest_distance = distance
            winning_key_size = key_size

    return winning_key_size

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
    def test_breaking_vigenere(self):
        filepath = os.path.dirname(os.path.abspath(__file__)) + '/files/challenge_6.txt'
        key = key_for_vigenere_cipher(filepath)
        expected = 'key'

        self.assertEqual(expected, key)

    def test_transpose_cipher_blocks_for_size(self):
        cipher_string = "0e3647e8592d35514a081243582536ed3de6734059001e3f535ce6271032"
        ciphertext = base64.b64decode(cipher_string)

        blocks = transpose_ciphertext_in_blocks_for_size(ciphertext, 2)

        expected = b'\xd1\xfa\xb7\xe7\x9d\x9e\xe1<n\xe7\xb9\xa7\xdd\xba~\xe74\xed\xe7\\\xad\xd7\xf6'
        self.assertEqual(expected, blocks[0])
        expected = b'\xed\xe3\xbc\xdd\xdfu\xad\xd77\xcd\xdf\x9d\xd7\xef4\xdd\xd5\xdf~{\xbbM'
        self.assertEqual(expected, blocks[1])

        cipher_string = "0e3647e8592d35514a081243582536ed3de6734059001e3f535ce6271032"
        ciphertext = base64.b64decode(cipher_string)

        blocks = transpose_ciphertext_in_blocks_for_size(ciphertext, 4)
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

        result = key_size_with_lowest_avg_ham_distance(ciphertext)
        self.assertEqual(2, result)

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
