import os
from single_byte_xor_cipher import decrypt_xor_cipher

def detect_xored_string(filepath):
    strings = list(map(lambda s: s.rstrip(), list(open(filepath, 'r'))))
    curr_score, decrypted, line_num = 0, '', 0

    for i, string in enumerate(strings):
        result = decrypt_xor_cipher(string)
        if result['score'] > curr_score:
            curr_score, line_num = result['score'], i
            decrypted = result['message']

    return f"It is the string on line number {line_num}. Decrypted message: {decrypted}"

print(detect_xored_string(os.path.dirname(os.path.abspath(__file__)) + '/files/challenge_4.txt'))
