# Write a function to generate a random AES key; that's just 16 random bytes.
# Write a function that encrypts data under an unknown key --- that is, a function
#    that generates a random key and encrypts under it.
# A function like encryption_oracle(your-input)
# Under the hood, have the function append 5-10 bytes (count chosen randomly)
#    before the plaintext and 5-10 bytes after the plaintext.
# Now, have the function choose to encrypt under ECB 1/2 the time, and under CBC the
#    other half (just use random IVs each time for CBC). Use rand(2) to decide which to use.
# Detect the block cipher mode the function is using each time. You should end
#    up with a piece of code that, pointed at a block box that might be encrypting
#    ECB or CBC, tells you which one is happening.

import random
import pkcs_7_padding
from Crypto.Cipher import AES
from cbc_mode import encrypt_with_aes_cbc_mode

MODE_ECB = 0
MODE_CBC = 1

BLOCK_SIZE = 16

def encryption_oracle(plaintext):
    key = random_bytes_of_size(BLOCK_SIZE).decode()

    # Append 5-10 random bytes before and after
    plaintext = random_bytes_of_size(random.randint(5, 11)) + plaintext
    plaintext = plaintext + random_bytes_of_size(random.randint(5, 11))
    plaintext = pkcs_7_padding.add_padding_by_block_size(plaintext, BLOCK_SIZE)

    ciphertext = encrypt_with_mode(key, plaintext, random.choice([MODE_ECB, MODE_CBC]))

    return ciphertext

def encrypt_with_mode(key, plaintext, mode):
    if mode == MODE_ECB:
        print("Processing in ECB mode...")
        return AES.new(key, AES.MODE_ECB).decrypt(plaintext)
    elif mode == MODE_CBC:
        print("Processing in CBC mode...")
        iv = random_initialization_vector(len(key))
        return encrypt_with_aes_cbc_mode(key, plaintext, iv)

def random_initialization_vector(size):
    return chr(random.randrange(0, 16)).encode() * size

def random_bytes_of_size(size):
    return b''.join(chr(random.randrange(32, 128)).encode() for _ in range(size))

plaintext = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam eleifend porta odio"\
        " sed rhoncus. Maecenas sed condimentum ligula, ut scelerisque magna. Pellentesque"\
        " posuere dolor id venenatis porta. Duis eget aliquet tortor. Suspendisse at est velit."\
        " Ut tortor felis, dignissim sed maximus ac, dictum eget nulla. Lorem ipsum dolor sit"\
        " amet, consectetur adipiscing elit. Sed sit amet dolor erat.".encode()

print(encryption_oracle(plaintext))
