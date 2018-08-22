def avg_hamming_distance_over_chunk_size(ciphertext, chunk_size):
    distances = []
    previous_chunk, previously_processed_chunk = b'', b''

    for chunk in chunks_by_size(ciphertext, chunk_size):
        if previous_chunk != previously_processed_chunk:
            distances.append(hamming_distance(previous_chunk, chunk) / chunk_size)
            previously_processed_chunk = chunk

        previous_chunk = chunk

    return sum(distances) / len(distances)

def hamming_distance(bytes1, bytes2):
    distance = 0

    for int1, int2 in zip(bytes1, bytes2):
        bin1, bin2 = '{:016b}'.format(int1), '{:016b}'.format(int2)
        distance += sum(bit1 != bit2 for bit1, bit2 in zip(bin1, bin2))

    return distance

def chunks_by_size(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
