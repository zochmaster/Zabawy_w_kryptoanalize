from kasiski import Kasiski
import itertools

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def clean_text(text):
    return ''.join([c for c in text.upper() if c in ALPHABET])

def vigenere_encrypt(text, key):
    text = text.upper()
    key = key.upper()
    result = ""
    key_index = 0
    for ch in text:
        if ch in ALPHABET:
            shift = ALPHABET.index(key[key_index % len(key)])
            idx = (ALPHABET.index(ch) + shift) % 26
            result += ALPHABET[idx]
            key_index += 1
        else:
            result += ch
    return result

def vigenere_decrypt(text, key):
    text = text.upper()
    key = key.upper()
    result = ""
    key_index = 0
    for ch in text:
        if ch in ALPHABET:
            shift = ALPHABET.index(key[key_index % len(key)])
            idx = (ALPHABET.index(ch) - shift) % 26
            result += ALPHABET[idx]
            key_index += 1
        else:
            result += ch
    return result

def vigenere_kasiski_attack(ciphertext, dictionary):
    cleaned = clean_text(ciphertext)
    kasiski = Kasiski(cleaned)
    candidates = kasiski.run_attack()

    if not candidates:
        return []

    results = []
    for length, _ in candidates[:5]:
        key = kasiski.find_key(length, dictionary, vigenere_decrypt)
        plain = vigenere_decrypt(ciphertext, key)

        words = plain.upper().split()
        score = sum(1 for word in words[:min(10, len(words))] if word in dictionary)


        results.append((key, score, plain))

        # Sortuj po liczbie trafień malejąco
        results.sort(key=lambda x: x[1], reverse=True)
        filtered = [(key, plain) for key, score, plain in results if score >= 3]

    return filtered


def vigenere_brute_force_attack(ciphertext, dictionary, max_key_length=5):
    ciphertext = ciphertext.upper()
    for length in range(1, max_key_length + 1):
        for key_tuple in itertools.product(ALPHABET, repeat=length):
            key = ''.join(key_tuple)
            decrypted = vigenere_decrypt(ciphertext, key)
            words = decrypted.upper().split()
            if all(word in dictionary for word in words[:min(5, len(words))]):
                return key, decrypted
    return None, None
