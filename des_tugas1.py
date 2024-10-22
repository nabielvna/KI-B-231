import base64
import random
import string

DES_TABLES = {
    # Initial Permutation
    "IP": [58, 50, 42, 34, 26, 18, 10, 2,
           60, 52, 44, 36, 28, 20, 12, 4,
           62, 54, 46, 38, 30, 22, 14, 6,
           64, 56, 48, 40, 32, 24, 16, 8,
           57, 49, 41, 33, 25, 17, 9, 1,
           59, 51, 43, 35, 27, 19, 11, 3,
           61, 53, 45, 37, 29, 21, 13, 5,
           63, 55, 47, 39, 31, 23, 15, 7],

    # Invers Initial Permutation
    "IP_INV": [40, 8, 48, 16, 56, 24, 64, 32,
               39, 7, 47, 15, 55, 23, 63, 31,
               38, 6, 46, 14, 54, 22, 62, 30,
               37, 5, 45, 13, 53, 21, 61, 29,
               36, 4, 44, 12, 52, 20, 60, 28,
               35, 3, 43, 11, 51, 19, 59, 27,
               34, 2, 42, 10, 50, 18, 58, 26,
               33, 1, 41, 9, 49, 17, 57, 25],

    # Permuted Choice 1
    "PC1": [57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4],

    # Permuted Choice 2
    "PC2": [14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32],

    # Expansion Permutation
    "E": [32, 1, 2, 3, 4, 5,
          4, 5, 6, 7, 8, 9,
          8, 9, 10, 11, 12, 13,
          12, 13, 14, 15, 16, 17,
          16, 17, 18, 19, 20, 21,
          20, 21, 22, 23, 24, 25,
          24, 25, 26, 27, 28, 29,
          28, 29, 30, 31, 32, 1],

    "S_BOXES": [
        # S1
        [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
        # S2
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
        # S3
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
        # S4
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
        # S5
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
        # S6
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
        # S7
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
        # S8
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
    ],

    # Permutation Function
    "P": [16, 7, 20, 21, 29, 12, 28, 17,
          1, 15, 23, 26, 5, 18, 31, 10,
          2, 8, 24, 14, 32, 27, 3, 9,
          19, 13, 30, 6, 22, 11, 4, 25]
}

# Random Key Generator
def generate_random_key():
    key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    return key

# Helper
def permute(block, table):
    return [block[i - 1] for i in table]

def split(block):
    return block[:len(block)//2], block[len(block)//2:]

def xor(a, b):
    return [x ^ y for x, y in zip(a, b)]

def left_shift(x, n):
    return x[n:] + x[:n]

def int_to_bits(n, bits):
    return [int(b) for b in format(n, f'0{bits}b')]

def bits_to_int(bits):
    return int(''.join(map(str, bits)), 2)

def string_to_bit_array(text):
    return [int(bit) for char in text.encode('utf-8') for bit in format(char, '08b')]

def bit_array_to_string(bits):
    return ''.join(chr(bits_to_int(bits[i:i+8])) for i in range(0, len(bits), 8))

# DES
def generate_subkeys(key):
    key = permute(key, DES_TABLES["PC1"])
    C, D = split(key)
    subkeys = []
    for i in range(16):
        if i in [0, 1, 8, 15]:
            C = left_shift(C, 1)
            D = left_shift(D, 1)
        else:
            C = left_shift(C, 2)
            D = left_shift(D, 2)
        subkey = permute(C + D, DES_TABLES["PC2"])
        subkeys.append(subkey)
    return subkeys

def f_function(R, subkey):
    expanded_R = permute(R, DES_TABLES["E"])
    xored = xor(expanded_R, subkey)
    S_output = []
    for i in range(8):
        block = xored[i*6:(i+1)*6]
        row = bits_to_int([block[0], block[5]])
        col = bits_to_int(block[1:5])
        S_output.extend(int_to_bits(DES_TABLES["S_BOXES"][i][row][col], 4))
    return permute(S_output, DES_TABLES["P"])

def des_round(L, R, subkey):
    return R, xor(L, f_function(R, subkey))

def des_encrypt(plaintext, key):
    subkeys = generate_subkeys(key)
    block = permute(plaintext, DES_TABLES["IP"])
    L, R = split(block)
    for subkey in subkeys:
        L, R = des_round(L, R, subkey)
    block = permute(R + L, DES_TABLES["IP_INV"])  
    return block

def des_decrypt(ciphertext, key):
    subkeys = generate_subkeys(key)
    block = permute(ciphertext, DES_TABLES["IP"])
    L, R = split(block)
    for subkey in reversed(subkeys):
        L, R = des_round(L, R, subkey)
    block = permute(R + L, DES_TABLES["IP_INV"])  
    return block

# Padding
def pad(text):
    pad_length = 8 - (len(text) % 8)
    return text + chr(pad_length) * pad_length

def unpad(text):
    pad_length = ord(text[-1])
    return text[:-pad_length]

# Enkrip & Dekrip
def encrypt(plaintext, key):
    padded_text = pad(plaintext)
    plaintext_bits = string_to_bit_array(padded_text)
    key_bits = string_to_bit_array(key[:8])  
    
    ciphertext_bits = []
    for i in range(0, len(plaintext_bits), 64):
        block = plaintext_bits[i:i+64]
        encrypted_block = des_encrypt(block, key_bits)
        ciphertext_bits.extend(encrypted_block)
    
    ciphertext_bytes = bytes(bits_to_int(ciphertext_bits[i:i+8]) for i in range(0, len(ciphertext_bits), 8))
    return base64.b64encode(ciphertext_bytes).decode('utf-8')

def decrypt(ciphertext, key):
    ciphertext_bytes = base64.b64decode(ciphertext)
    ciphertext_bits = [int(bit) for byte in ciphertext_bytes for bit in format(byte, '08b')]
    key_bits = string_to_bit_array(key[:8]) 
    
    plaintext_bits = []
    for i in range(0, len(ciphertext_bits), 64):
        block = ciphertext_bits[i:i+64]
        decrypted_block = des_decrypt(block, key_bits)
        plaintext_bits.extend(decrypted_block)
    
    plaintext = bit_array_to_string(plaintext_bits)
    return unpad(plaintext)

# main
def main():
    key = generate_random_key()
    plaintext = "COBA APA AJA"
    
    print("Plaintext:", plaintext)
    print("Key:", key)
    
    # Enkripsi
    ciphertext = encrypt(plaintext, key)
    print("Ciphertext:", ciphertext)
    
    # Dekripsi
    decrypted_text = decrypt(ciphertext, key)
    print("Decrypted text:", decrypted_text)
    
    if decrypted_text == plaintext:
        print("Encryption and decryption successful!")
    else:
        print("Something went wrong.")

if __name__ == "__main__":
    main();