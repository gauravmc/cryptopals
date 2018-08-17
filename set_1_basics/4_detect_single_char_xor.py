from single_byte_xor_cipher import decrypt_xor_cipher

def detect_xored_string(filepath):
    curr_score, message, line_num = 0, '', 0

    with open(filepath) as f:
        for i, line in enumerate(f):
            result = decrypt_xor_cipher(line.rstrip())
            if result['score'] > curr_score:
                curr_score, line_num = result['score'], i
                message = result['message'].strip()

    return f"It is the string on line number {line_num}. Decrypted message: {message}"

print(detect_xored_string(os.path.dirname(os.path.abspath(__file__)) + '/files/challenge_4.txt'))
