import struct
import sys

def compress(content):
    # Convert content to bytes
    content = bytes(content, 'utf-8')

    # LZW Compression Algorithm
    dictionary = {bytes([i]): i for i in range(256)}
    current_code = 256
    buffer = b""
    compressed_data = []

    for byte in content:
        new_buffer = buffer + bytes([byte])
        if new_buffer in dictionary:
            buffer = new_buffer
        else:
            # append code for current buffer to compressed data
            compressed_data.append(dictionary[buffer])
            # add new buffer to dictionary if possible
            if current_code < 65536:
                dictionary[new_buffer] = current_code
                current_code += 1
            buffer = bytes([byte])

    if buffer in dictionary:
        # append code for final buffer to compressed data
        compressed_data.append(dictionary[buffer])

    # Convert codes to bytes and write compressed data to output file
    compressed_bytes = b''
    for code in compressed_data:
        compressed_bytes += struct.pack("<H", code)

    # Calculate and print compression ratio
    original_size = len(content)
    compressed_size = len(compressed_bytes)
    ratio = compressed_size / original_size
    #print(f"Compression ratio: {ratio:.2%}")

    return compressed_bytes


# Get the input string from the command line arguments
input_string = sys.argv[1]

# Call the compress_string function and write the compressed string to the standard output
compressed_string = compress(input_string)
sys.stdout.buffer.write(compressed_string)