# Decryption Function (improved)
def ntru_decrypt(ciphertext, f, N, p, q):
    # Decrypt by multiplying the ciphertext by the private key polynomial
    a = poly_mult_mod(ciphertext, f, q)
    a = (a + q) % q  # Ensure positive coefficients
    decrypted_message = np.mod(a, p)  # Get the decrypted message mod p
    decrypted_text = binary_to_text(decrypted_message[:N])  # Pass only N terms to binary_to_text
    return decrypted_text


# Text to binary (encoding function)
def text_to_binary(text):
    binary_string = ''.join(format(ord(char), '08b') for char in text)
    # Convert binary string to array of integers (1 or 0)
    return np.array([int(bit) for bit in binary_string], dtype=int)
