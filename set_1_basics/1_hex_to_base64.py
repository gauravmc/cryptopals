import base64

# Always operate on raw bytes, never on encoded strings. Only use hex and base64 for pretty-printing.

def hex_to_base64(encoded_str):
    return base64.b64encode(bytes.fromhex(encoded_str))

# print(hex_to_base64('49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'))
