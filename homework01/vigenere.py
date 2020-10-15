def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    
    keyword = keyword.lower()
    
    for i in range(len(plaintext)):
        c_text = plaintext[i]
        c_key = keyword[i % len(keyword)]

        if not c_text.isalpha():
            ciphertext += c_text
            continue

        upper = c_text.isupper()
        c_text = c_text.lower()
        
        nc = ord(c_text) - ord('a')
        shift = ord(c_key) - ord('a')
        nc = (nc + shift) % 26
        c_text = chr(nc + ord('a'))

        if upper:
            c_text = c_text.upper()

        ciphertext += c_text


    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""

    keyword = keyword.lower()
    
    for i in range(len(ciphertext)):
        c_text = ciphertext[i]
        c_key = keyword[i % len(keyword)]

        if not c_text.isalpha:
            plaintext += c_text
            continue

        upper = c_text.isupper()
        c_text = c_text.lower()

        nc = ord(c_text) - ord('a') 
        shift = ord(c_key) - ord('a')
        nc -= shift
        if nc < 0:
            nc += 26

        c_text = chr(nc + ord('a'))

        if upper:
            c_text = c_text.upper()

        plaintext += c_text

    return plaintext
