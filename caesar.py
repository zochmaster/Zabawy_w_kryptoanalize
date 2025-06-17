# Alfabet używany w szyfrze Cezara – tylko wielkie litery od A do Z
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Funkcja szyfrująca tekst za pomocą szyfru Cezara
# Argumenty:
#   text – tekst wejściowy do zaszyfrowania
#   key – liczba pozycji o którą każda litera zostanie przesunięta w prawo
def caesar_encrypt(text, key):
    text = text.upper()          # konwersja tekstu do wielkich liter
    result = ""                  # zmienna do przechowywania wyniku szyfrowania

    for ch in text:              # iteracja po każdym znaku w tekście
        if ch in ALPHABET:
            # obliczenie nowej pozycji litery po przesunięciu
            idx = (ALPHABET.index(ch) + key) % len(ALPHABET)
            result += ALPHABET[idx]  # dodanie zaszyfrowanej litery do wyniku
        else:
            # jeżeli znak nie należy do alfabetu (np. spacja, interpunkcja), zostaje bez zmian
            result += ch

    return result  # zwrócenie zaszyfrowanego tekstu

# Funkcja deszyfrująca tekst zaszyfrowany szyfrem Cezara
# Deszyfrowanie polega na przesunięciu liter w przeciwnym kierunku
def caesar_decrypt(text, key):
    # Wywołanie funkcji szyfrującej z przeciwnym przesunięciem (ujemnym kluczem)
    return caesar_encrypt(text, -key % len(ALPHABET))
