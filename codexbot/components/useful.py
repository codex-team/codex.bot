def grouped(sequence, chunk_size):
    return [sequence[i:i + chunk_size] for i in range(0, len(sequence), chunk_size)]
