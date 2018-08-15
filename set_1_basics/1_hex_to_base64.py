import codecs, base64

# Always operate on raw bytes, never on encoded strings. Only use hex and base64 for pretty-printing.

def hex_to_base64(str):
    return base64.b64encode(codecs.decode(str, 'hex'))
