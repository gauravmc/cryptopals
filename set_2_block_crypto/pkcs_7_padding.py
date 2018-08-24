import unittest

class SizeNotSupportedError(Exception): pass

def add_padding_by_block_size(plaintext, block_size):
    if (len(plaintext) % block_size != 0):
        expected_size = len(plaintext) + (block_size - len(plaintext) % block_size)
        return add_padding(plaintext, expected_size)
    else:
        return plaintext

def add_padding(block, expected_block_size):
    padding_size = expected_block_size - len(block)
    if padding_size > 256:
        raise SizeNotSupportedError("PKCS#7 only works if padding size is less than 256")
    padding = chr(padding_size).encode() * padding_size
    return block + padding

class TestSet2Challenge9(unittest.TestCase):
    def test_value_of_padded_bye_is_as_per_size_of_padding_required(self):
        block = 'YELLOW SUBMARINE'.encode()
        expected = b'YELLOW SUBMARINE\x04\x04\x04\x04'
        self.assertEqual(expected, add_padding(block, 20))

        block = 'YELLOW SUBMARINE'.encode()
        expected = b'YELLOW SUBMARINE\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'
        self.assertEqual(expected, add_padding(block, 32))

    def test_add_pkcs_padding_by_block_size(self):
        plaintext = "Lorem ipsum dolor sit amet, consectetur adipiscing elit.".encode()
        result = add_padding_by_block_size(plaintext, 16)

        expected = b'Lorem ipsum dolor sit amet, consectetur adipiscing elit.\x08\x08\x08\x08\x08\x08\x08\x08'
        self.assertEqual(expected, result)

        # Sample text that doesn't need padding
        plaintext = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam el.".encode()
        result = add_padding_by_block_size(plaintext, 16)

        self.assertEqual(plaintext, result)

    def test_size_larger_than_256_unsupported(self):
        with self.assertRaises(SizeNotSupportedError):
            block = 'YELLOW SUBMARINE'.encode()
            add_padding(block, len(block) + 257)

if __name__ == '__main__':
    unittest.main()
