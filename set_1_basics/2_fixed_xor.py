import codecs

def buffer_xor(buffer1, buffer2):
    buffer1 = codecs.decode(buffer1, 'hex')
    buffer2 = codecs.decode(buffer2, 'hex')

    result = bytearray()

    for byte1, byte2 in zip(buffer1, buffer2):
        result.append(byte1 ^ byte2)

    return codecs.encode(result, 'hex')

# print(buffer_xor('1c0111001f010100061a024b53535009181c', '686974207468652062756c6c277320657965'))
