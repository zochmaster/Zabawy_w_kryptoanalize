import numpy as np
from itertools import product
from math import gcd
from textwrap import wrap
from dictionary import check_words_in_dict
from utils import is_probably_english
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Konwertuje tekst do postaci listy liczb odpowiadających pozycjom liter w alfabecie (A=0, ..., Z=25)
# Ignoruje znaki spoza alfabetu
def text_to_numbers(text):
    return [ALPHABET.index(c) for c in text if c.upper() in ALPHABET]

# Zamienia listę liczb (0–25) na odpowiadające im litery alfabetu
# Używa modulo 26, aby obsłużyć ewentualne wartości spoza zakresu
def numbers_to_text(numbers):
    return "".join(ALPHABET[n % 26] for n in numbers)

# Wstawia znaki niebędące literami (np. spacje, przecinki) z oryginalnego tekstu
# z powrotem do przetworzonego tekstu z literami
# Przykład: original="HELLO, WORLD", processed="ABCDEF" → wynik="ABCDEF, "
def preserve_non_letters(original_text, processed_letters):
    result = []
    j = 0
    for char in original_text:
        if char.upper() in ALPHABET:
            result.append(processed_letters[j])
            j += 1
        else:
            result.append(char)
    return ''.join(result)

# Szyfruje tekst za pomocą szyfru Hilla z użyciem podanej macierzy klucza
# Argumenty:
#   text – tekst do zaszyfrowania
#   key_matrix – lista liczb całkowitych reprezentujących macierz klucza (rozmiar NxN)
# Zwraca:
#   zaszyfrowany tekst jako ciąg liter
def hill_encrypt(text, key_matrix):
    size = int(len(key_matrix) ** 0.5)
    matrix = np.array(key_matrix).reshape((size, size))
    text_nums = text_to_numbers(text.upper())

    # Dopełnienie zerami, jeśli liczba znaków nie dzieli się przez rozmiar macierzy
    if len(text_nums) % size != 0:
        text_nums += [0] * (size - len(text_nums) % size)

    ciphertext = []
    for i in range(0, len(text_nums), size):
        block = np.array(text_nums[i:i+size])
        enc_block = matrix.dot(block) % 26
        ciphertext.extend(enc_block)

    return numbers_to_text(ciphertext)

# Oblicza odwrotną macierz modulo 26
# Jeśli macierz nie ma odwrotności – rzuca wyjątek
def mod_inverse_matrix(matrix, mod=26):
    det = int(round(np.linalg.det(matrix)))
    det_mod = det % mod
    inv_det = mod_inverse(det_mod, mod)
    if inv_det is None:
        raise ValueError("Macierz nieodwracalna.")

    # Obliczanie macierzy dopełnień algebraicznych
    cofactors = np.zeros_like(matrix)
    n = matrix.shape[0]
    for r in range(n):
        for c in range(n):
            minor = np.delete(np.delete(matrix, r, axis=0), c, axis=1)
            cofactors[r, c] = ((-1) ** (r + c)) * int(round(np.linalg.det(minor)))

    # Transpozycja i pomnożenie przez odwrotność wyznacznika
    adjugate = cofactors.T % mod
    return (inv_det * adjugate) % mod

# Deszyfruje tekst zaszyfrowany szyfrem Hilla
# Argumenty:
#   ciphertext – tekst zaszyfrowany
#   key_matrix – oryginalna macierz klucza
# Zwraca:
#   tekst jawny po deszyfrowaniu
def hill_decrypt(ciphertext, key_matrix):
    size = int(len(key_matrix) ** 0.5)
    matrix = np.array(key_matrix).reshape((size, size))
    inv_matrix = mod_inverse_matrix(matrix)
    text_nums = text_to_numbers(ciphertext.upper())

    if len(text_nums) % size != 0:
        text_nums += [0] * (size - len(text_nums) % size)

    plaintext = []
    for i in range(0, len(text_nums), size):
        block = np.array(text_nums[i:i+size])
        dec_block = inv_matrix.dot(block) % 26
        plaintext.extend(dec_block)

    return numbers_to_text(plaintext)

# Oblicza liczbę słów w tekście, które występują w słowniku
# Służy do oceny prawdopodobieństwa poprawnego odszyfrowania
def score_decryption(text, dictionary):
    words = text.upper().split()
    return len(set(w for w in words if w in dictionary))

# Przeprowadza brute-force atak na szyfr Hilla (2x2 lub 3x3)
# Przegląda wszystkie możliwe odwracalne macierze klucza i testuje je
# Zwraca do 'top_n' najlepiej ocenionych odszyfrowań
def hill_brute_force_attack(ciphertext, dictionary, top_n=5, threshold=0.75, size=2):
    top_results = []
    dim = size * size  # liczba elementów w macierzy (np. 4 dla 2x2)

    for perm in product(range(26), repeat=dim):
        try:
            matrix = np.array(perm).reshape((size, size))
            det = round(np.linalg.det(matrix)) % 26
            if gcd(int(det), 26) != 1:
                continue  # pomiń macierze bez odwrotności

            raw = hill_decrypt(ciphertext, list(perm))
            decrypted = preserve_non_letters(ciphertext, raw).upper()

            # Sprawdzenie, czy wynik wygląda jak język angielski
            if is_probably_english(decrypted, threshold=threshold):
                if decrypted not in [res[1] for res in top_results]:
                    top_results.append((list(perm), decrypted))
                    if len(top_results) >= top_n:
                        break  # zakończ wcześniej dla wydajności

        except Exception:
            continue

    if not top_results:
        return "No valid key found in brute force."

    result_str = ""
    for key, plain in top_results:
        result_str += f"Key: {key}\nPlaintext: {plain}\n\n"

    return result_str.strip()

# Znajduje odwrotność liczby a modulo m (jeśli istnieje)
# Zwraca x, takie że (a * x) % m == 1
def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# Sprawdza, czy dana płaska lista liczb tworzy macierz odwracalną modulo 26
def is_invertible_matrix(matrix_flat, size):
    if len(matrix_flat) != size * size:
        return False
    matrix = np.array(matrix_flat).reshape((size, size))
    det = int(round(np.linalg.det(matrix))) % 26
    return gcd(det, 26) == 1 and mod_inverse(det, 26) is not None
