import tkinter as tk
from tkinter import messagebox
import numpy as np

# Parameters for NTRU-like scheme
N = 11  # Polynomial degree (small for example purposes)
p = 3  # Small modulus for plaintext coefficients
q = 32  # Large modulus for ciphertext coefficients

# User data structure (this can be extended for multiple users)
users = {
    "unit1": {},
    "unit2": {},
    "headquarters": {}
}

current_user = None
