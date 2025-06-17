import re
from itertools import product

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Kasiski:
    def __init__(self, text):
        # Usuwa znaki spoza alfabetu i konwertuje tekst do wielkich liter
        self.abc = ALPHABET
        self.text = ''.join(c for c in text.upper() if c in self.abc)

    def find_distance_between_sequences(self):
        # Wyszukuje powtarzające się sekwencje długości 3–5
        # i oblicza odległości między ich kolejnymi wystąpieniami
        sequences = {}
        for i in range(len(self.text)):
            for j in range(3, 6):  # długość sekwencji: 3, 4, 5
                if i + j <= len(self.text):
                    seq = self.text[i:i + j]
                    sequences.setdefault(seq, []).append(i)

        distances = []
        for positions in sequences.values():
            if len(positions) > 1:
                # dodaj różnice pozycji kolejnych wystąpień
                for i in range(len(positions) - 1):
                    distances.append(positions[i + 1] - positions[i])
        return distances

    def get_primefactors(self, number):
        # Generator zwracający czynniki pierwsze podanej liczby
        i = 2
        while i * i <= number:
            while number % i == 0:
                yield i
                number //= i
            i += 1
        if number > 1:
            yield number

    def get_candidate_key_lengths(self, distances):
        # Zbiera wszystkie czynniki pierwsze z listy odległości
        # i zwraca najczęściej występujące jako kandydatów na długość klucza
        factors = []
        for d in distances:
            factors.extend(self.get_primefactors(d))
        freq = {}
        for f in factors:
            freq[f] = freq.get(f, 0) + 1
        return sorted(freq.items(), key=lambda x: x[1], reverse=True)

    def find_most_used_char(self, row, keylength):
        # Zlicza najczęściej występującą literę w danej kolumnie tekstu
        # (czyli modulo pozycji względem długości klucza)
        frequency = {}
        for i in range(row, len(self.text), keylength):
            c = self.text[i]
            if c in self.abc:
                frequency[c] = frequency.get(c, 0) + 1
        return max(frequency, key=frequency.get, default='E')

    def find_key(self, keylength, dictionary, decrypt_func):
        # Przeszukuje możliwe przesunięcia klucza na podstawie
        # porównań najczęstszych liter z literami referencyjnymi (E, T, A, ...)
        # i wybiera klucz dający najlepszy wynik słownikowy
        reference_letters = ['E', 'T', 'A', 'O', 'N', 'R']
        best_score = -1
        best_key = ""

        for refs in product(reference_letters, repeat=keylength):
            key = ""
            for i in range(keylength):
                most_common = self.find_most_used_char(i, keylength)
                shift = (self.abc.index(most_common) - self.abc.index(refs[i])) % len(self.abc)
                key += self.abc[shift]

            decrypted = decrypt_func(self.text, key)
            words = decrypted.upper().split()
            score = sum(1 for w in words[:min(8, len(words))] if w in dictionary)

            if score > best_score:
                best_score = score
                best_key = key

        return best_key

    def run_attack(self):
        # Główna funkcja: uruchamia atak Kasiski
        # Zwraca posortowaną listę kandydatów na długość klucza
        distances = self.find_distance_between_sequences()
        if not distances:
            return []
        return self.get_candidate_key_lengths(distances)
