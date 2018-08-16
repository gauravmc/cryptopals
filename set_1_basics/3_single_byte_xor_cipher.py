def decrypt_xor_cipher(encoded_str):
    string = bytes.fromhex(encoded_str)

    curr_score, message, key_char = 0, '', 0

    for i in range(0, 128):
        xored_msg = xor_byte_with_buffer(i, string).decode()
        score = frequency_analysis_score(xored_msg)
        if score > curr_score:
            curr_score, message, key_char = score, xored_msg, i

    return key_char, message

ENGLISH_LETTER_FREQ = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'

def frequency_analysis_score(msg):
    msg = msg.upper()

    letter_freq = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
    for letter in msg:
        if letter in letter_freq:
            letter_freq[letter] += 1

    sorted_letter_list = sorted(letter_freq.items(), key=lambda t : t[1], reverse=True)
    ordered_letters = ''
    for lett, _ in sorted_letter_list:
        ordered_letters += lett[0]

    return get_etaoin_score(ordered_letters)

def get_etaoin_score(letters):
    score = 0

    for letter in ETAOIN[:6]:
        if letter in letters[:6]:
            score += 1

    for letter in ETAOIN[-6:]:
        if letter in letters[-6:]:
            score += 1

    return score

def xor_byte_with_buffer(byte, str_bytes):
    return bytes(str_b ^ byte for str_b in str_bytes)

# print(decrypt_xor_cipher('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'))
