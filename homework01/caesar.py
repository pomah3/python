import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    
    for c in plaintext:
        if not c.isalpha():
            ciphertext += c
            continue
        
        isupper = c.isupper()
        c = c.lower()

        nc = ord(c) - ord('a')
        nc = (nc + shift) % 26        
        c = chr(nc + ord('a'))

        if isupper:
            c = c.upper()

        ciphertext += c

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""

    for c in ciphertext:
        if not c.isalpha():
            plaintext += c
            continue
        
        isupper = c.isupper()
        c = c.lower()

        nc = ord(c) - ord('a')
        nc = nc - shift 
        if nc < 0:
            nc += 26  
        c = chr(nc + ord('a'))

        if isupper:
            c = c.upper()

        plaintext += c
    
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
