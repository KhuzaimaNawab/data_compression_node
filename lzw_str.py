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
input_string = sys.argv[1]

# Call the compress_string function and write the compressed string to the standard output
compressed_string = compress(input_string)
sys.stdout.buffer.write(compressed_string)

# print(compress("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec pellentesque nisi vel libero accumsan, nec vulputate erat auctor. Ut eget ultricies leo. Mauris facilisis vehicula sapien non vehicula. Integer laoreet dui at risus tincidunt pharetra. Ut vestibulum diam ac est efficitur blandit. Mauris vel eleifend neque, at finibus eros. Duis quis imperdiet orci.Cras fringilla, leo ut sollicitudin convallis, nulla nisl volutpat diam, et mattis quam ipsum in metus. Ut placerat varius tellus vitae tincidunt. Curabitur ultrices interdum arcu quis viverra. Fusce est est, interdum at nulla vitae, rhoncus sagittis eros. In ut placerat nunc, sit amet interdum dui. Ut feugiat dolor turpis, nec varius orci ullamcorper at. Aenean vehicula quis magna sed sollicitudin. Vivamus pretium purus neque, vel mollis nunc sodales pharetra. Maecenas at tempor sem, non hendrerit tortor. Phasellus nec ullamcorper ipsum. Duis laoreet diam vel metus aliquet, vel elementum dolor interdum. Fusce lobortis nunc sed dui mollis, ac rhoncus velit facilisis.Suspendisse lacinia hendrerit lectus non accumsan. Maecenas imperdiet orci eget dignissim venenatis. Proin elementum dignissim elit, nec bibendum nisi ornare et. Ut blandit ornare elit nec mollis. Suspendisse sem neque, aliquam ut neque non, pharetra volutpat dui. Mauris ultrices, mi ut commodo interdum, nisi sem efficitur enim, nec tincidunt dolor mi eget lacus. Nunc imperdiet nibh id hendrerit congue. Morbi scelerisque quam sed ante blandit sollicitudin. Vestibulum luctus laoreet pulvinar. Mauris eget nisi tellus. Fusce et posuere lacus. Nulla facilisi. Phasellus feugiat molestie molestie. Proin sollicitudin libero dui, in rhoncus augue commodo vel.Donec ac malesuada orci. In hac habitasse platea dictumst. Curabitur mauris felis, aliquet sed felis ut, venenatis laoreet libero. Curabitur et urna scelerisque, rutrum mauris quis, finibus lorem. Cras dapibus velit ipsum, mattis feugiat felis ullamcorper vitae. Quisque nec eleifend lectus. Praesent congue nisl vitae eros porta, ac porta ex bibendum. Etiam tristique dictum suscipit. Proin sed lacus nec nunc luctus malesuada sed eget sapien. Quisque blandit purus massa, eget tempus felis pretium eget. Donec eget tempor tortor. Aenean sagittis ornare ex, at consectetur mi finibus at.Praesent eget egestas dolor. Phasellus vel ex in dolor luctus suscipit sed vitae ipsum. Vestibulum in semper purus, nec pharetra lectus. Pellentesque vel mattis lectus, sit amet consectetur mauris. Nullam est massa, rutrum vitae nisi at, congue ullamcorper est. Nullam a egestas leo. Suspendisse varius eros quis est aliquet dictum. Ut blandit dui sit amet pellentesque interdum. ."))