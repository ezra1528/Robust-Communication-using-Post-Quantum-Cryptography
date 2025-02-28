# Polynomial multiplication mod q (updated)
def poly_mult_mod(poly1, poly2, q):
    result = np.convolve(poly1, poly2) % q  # Convolution of polynomials
    return result[:N]  # Truncate to N terms for simplicity


# Encryption Function (fixed)
def ntru_encrypt(message, h, N, p, q):
    m_poly = text_to_binary(message)

    # Ensure message fits into the polynomial size
    if len(m_poly) < N:
        m_poly = np.pad(m_poly, (0, N - len(m_poly)), 'constant')
    elif len(m_poly) > N:
        m_poly = m_poly[:N]

    r = np.random.randint(-1, 2, N)  # Random polynomial for encryption

    ciphertext = (poly_mult_mod(r, h, q) + m_poly) % q  # Final ciphertext
    return ciphertext

