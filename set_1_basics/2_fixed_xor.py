def string_buffer_xor(buffer1, buffer2):
    s1 = bytes.fromhex(buffer1)
    s2 = bytes.fromhex(buffer2)

    return bytes(b1 ^ b2 for b1, b2 in zip(s1, s2)).hex()

# print(string_buffer_xor('1c0111001f010100061a024b53535009181c', '686974207468652062756c6c277320657965'))
