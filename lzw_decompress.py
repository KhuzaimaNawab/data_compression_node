import struct
import sys

def decompress(content):
    # Convert content to codes
    codes = []
    for i in range(0, len(content), 2):
        code = struct.unpack("<H", content[i:i+2])[0]
        codes.append(code)

    # LZW Decompression Algorithm
    dictionary = {i: bytes([i]) for i in range(256)}
    current_code = 256
    buffer = b""
    decompressed_data = []

    for code in codes:
        if code not in dictionary:
            # special case for the first code
            if not buffer:
                buffer = dictionary[code-1]
            else:
                dictionary[current_code] = buffer + bytes([buffer[0]])
                current_code += 1
            decompressed_data.append(buffer + bytes([buffer[0]]))
        else:
            decompressed_data.append(dictionary[code])
            if buffer:
                dictionary[current_code] = buffer + \
                    bytes([dictionary[code][0]])
                current_code += 1
        buffer = dictionary[code]

    # Convert integers back to bytes
    decompressed_data_bytes = []
    for data in decompressed_data:
        if isinstance(data, int):
            data = struct.pack('B', data)
        decompressed_data_bytes.append(data)

    # Write decompressed data to output file
    decompressed_content = b"".join(decompressed_data_bytes).decode('utf-8')

    return decompressed_content


# Get the input string from the command line arguments
input_string = sys.argv[1].encode().decode('unicode_escape').encode()

# Call the compress_string function and write the compressed string to the standard output
decompressed_string = decompress(input_string)