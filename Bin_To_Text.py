# Binary to text (decoding function with error handling for valid binary data)
def binary_to_text(binary_array):
    # Convert binary array to a string
    binary_string = ''.join(map(str, binary_array))

    # Ensure length is a multiple of 8
    if len(binary_string) % 8 != 0:
        binary_string = binary_string[:-(len(binary_string) % 8)]

    # Split binary string into 8-bit chunks (1 byte each)
    bytes_list = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]

    # Convert binary chunks to characters
    text = ''
    for byte in bytes_list:
        try:
            text += chr(int(byte, 2))
        except ValueError:
            return "Decryption Error: Invalid binary data"
    return text

