import string

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Usuwa znaki spoza alfabetu i konwertuje tekst do wielkich liter.
# Przykład: "Hello, World!" → "HELLOWORLD"
def clean_text(text):
    return ''.join(filter(str.isalpha, text.upper()))

# Wstawia znaki niebędące literami (np. spacje, przecinki) z oryginalnego tekstu
# z powrotem do przetworzonego tekstu z literami.
# Przykład: original = "A B!", processed = "XYZ" → wynik = "X Y!"
def format_with_spaces(original, processed):
    result, idx = [], 0
    for char in original:
        if char.upper() in ALPHABET:
            result.append(processed[idx])
            idx += 1
        else:
            result.append(char)
    return ''.join(result)

# Przesuwa literę 'c' o 'shift' pozycji w prawo (modulo 26).
# Przykład: shift_char('A', 3) → 'D'
def shift_char(c, shift):
    return ALPHABET[(ALPHABET.index(c) + shift) % len(ALPHABET)]

# Przesuwa literę 'c' o 'shift' pozycji w lewo (modulo 26).
# Przykład: unshift_char('D', 3) → 'A'
def unshift_char(c, shift):
    return ALPHABET[(ALPHABET.index(c) - shift) % len(ALPHABET)]

# Wczytuje słownik słów z pliku "english_words.txt" do zbioru.
# Każde słowo jest konwertowane do wielkich liter i oczyszczone z białych znaków.
with open("english_words.txt") as f:
    ENGLISH_WORDS = set(word.strip().upper() for word in f if word.strip())

# Sprawdza, czy dane słowo znajduje się w załadowanym słowniku.
def is_english_word(word):
    return word.upper() in ENGLISH_WORDS

# Ocenia prawdopodobieństwo, że tekst jest angielski na podstawie słownika.
# Porównuje pierwsze 5 słów z tekstu z zawartością słownika i sprawdza,
# czy odsetek pasujących słów przekracza ustalony próg.
# Zwraca True, jeśli warunek spełniony.
def is_probably_english(text, threshold=0.5):
    words = text.upper().split()
    if not words:
        return False
    sample = words[:min(5, len(words))]
    return sum(1 for w in sample if is_english_word(w)) / len(sample) >= threshold
