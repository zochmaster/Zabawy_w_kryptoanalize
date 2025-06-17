from collections import Counter  # do analizy częstotliwości liter
from caesar import caesar_decrypt  # deszyfrowanie szyfrem Cezara
from dictionary import check_words_in_dict  # sprawdzanie poprawnych słów

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Atak częstotliwościowy na szyfr Cezara z obowiązkową walidacją słownikową
# Argumenty:
#   ciphertext – tekst zaszyfrowany
#   dictionary – zbiór angielskich słów (typ: set)
# Zwraca:
#   (klucz, odszyfrowany tekst) – albo ostrzeżenie, jeśli tekst nie przejdzie walidacji
def caesar_frequency_attack(ciphertext, dictionary):
    # Zachowujemy tylko litery z alfabetu, ignorując cyfry i znaki interpunkcyjne
    filtered = ''.join([c for c in ciphertext.upper() if c in ALPHABET])

    if not filtered:
        return None, "No valid characters to analyze."

    # Liczymy częstość występowania każdej litery
    freq = Counter(filtered)
    most_common_letter, _ = freq.most_common(1)[0]

    # Zakładamy, że najczęstsza litera w szyfrogramie odpowiada 'E'
    assumed_shift = (ALPHABET.index(most_common_letter) - ALPHABET.index('E')) % 26

    # Deszyfrujemy szyfrogram przy użyciu odgadniętego klucza
    decrypted = caesar_decrypt(ciphertext, assumed_shift)

    # Weryfikacja słownikowa – czy tekst zawiera co najmniej 5 poprawnych słów
    if check_words_in_dict(decrypted, dictionary, 5):
        return assumed_shift, decrypted
    else:
        return assumed_shift, "[WARN] Decrypted text failed dictionary check:\n" + decrypted
