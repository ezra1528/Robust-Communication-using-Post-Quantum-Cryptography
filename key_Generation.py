# Key Generation for NTRU (simplified without inversion)
def generate_ntru_keys(N, p, q):
    f = np.random.randint(-1, 2, N)  # Small coefficients for private key
    g = np.random.randint(-1, 2, N)  # Another small polynomial for public key

    # Ensure f and g are not all-zero
    while not np.any(f):
        f = np.random.randint(-1, 2, N)
    while not np.any(g):
        g = np.random.randint(-1, 2, N)

    # Create public key h as (p * g) mod q
    h = (p * g) % q  # Simplified public key
    return f, h  # Returning coefficients for simplicity
