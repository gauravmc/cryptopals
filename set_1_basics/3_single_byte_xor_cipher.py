from collections import OrderedDict

def decrypt_xor_cipher(encoded_str):
    string = bytes.fromhex(encoded_str)

    curr_score = 0
    message, key_char = '', 0

    for i in range(0, 256):
        curr_message = single_char_xor(i, string).decode('utf-8', 'ignore')
        score = frequency_analysis_score(curr_message)
        if score > curr_score:
            curr_score = score
            message, key_char = curr_message, i

    return message, key_char

def frequency_analysis_score(msg):
    msg = msg.upper()

    letter_freq = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}
    for char in msg:
        if char in letter_freq:
            letter_freq[char] += 1

    letter_freq = OrderedDict(sorted(letter_freq.items(), key=lambda t: t[1], reverse=True))
    ordered_letters = ''.join(letter_freq.keys())
    return get_etaoin_score(ordered_letters)

ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'

def get_etaoin_score(letters):
    score = 0

    for letter in ETAOIN[:6]:
        if letter in letters[:6]:
            score += 1

    for letter in ETAOIN[-6:]:
        if letter in letters[-6:]:
            score += 1

    return score

def single_char_xor(char, str_bytes):
    return bytes(str_b ^ char for str_b in str_bytes)

# print(decrypt_xor_cipher('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'))
