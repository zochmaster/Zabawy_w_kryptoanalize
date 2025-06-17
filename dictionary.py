# Wczytuje słownik angielskich słów z pliku tekstowego.
# Każde słowo jest konwertowane do wielkich liter i dodawane do zbioru.
# Domyślnie plik to "english_words.txt".
def load_dictionary(file_path="english_words.txt"):
    with open(file_path, "r") as f:
        return set(word.strip().upper() for word in f.readlines())

# Sprawdza, czy tekst zawiera co najmniej 'n' słów obecnych w słowniku.
# Tekst jest dzielony na słowa po spacjach, a każde porównywane do słownika (bez interpunkcji).
# Zwraca True, jeśli znajdzie się wystarczająca liczba unikalnych dopasowań.
def check_words_in_dict(text, dictionary, n=5):
    words = text.upper().split()
    unique = set(w for w in words if w in dictionary)
    return len(unique) >= n
