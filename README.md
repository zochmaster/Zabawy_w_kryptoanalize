# Zabawa w kryptoanalizę

Projekt stworzony w ramach praktyk, którego celem jest szyfrowanie, rozszyfrowywanie i łamanie szyfrów Cezara, Vigenere'a oraz Hilla. 
Program zawiera GUI pozwalające łatwiej z niego korzystać.

# Funkcje:

## Obsługiwane szyfry:
  - *Cezar*  
  Szyfrowanie i deszyfrowanie z przesunięciem o klucz liczbowy (0-25).
  Dostępne ataki: brute-force, analiza częstotliwości.

  - *Vigenère*  
  Klasyczny szyfr polialfabetyczny z kluczem słownym. 
  Dostępne ataki: Kasiski, brute-force, tryb automatyczny (Kasiski + brute-force).

  - *Hill*  
  Szyfrowanie blokowe z użyciem macierzy klucza (2x2 lub 3x3). 
  Atak: brute-force z analizą językową.

## Inne funkcjonalności:
  - Automatyczne czyszczenie tekstu z nie-alfabetycznych znaków (przy atakach).
  - Weryfikacja poprawności macierzy klucza Hilla.
  - Wbudowany słownik języka angielskiego do analizy trafności.
  - Czytelne komunikaty debugujące w konsoli.

# Uruchamianie
  ## Wymagania

  - Python 3.8 lub nowszy
  - Biblioteki:
    - numpy (do obliczeń macierzowych w szyfrze Hilla)
    - tkinter (zazwyczaj dostępny domyślnie z Pythonem)

  1. Upewnij się, że masz zainstalowanego Pythona 3.8+
  2. Zainstaluj wymagane biblioteki
  3. Uruchom GUI:
    ```bash
    python main_gui.py
    ```

# Struktura projektu

- `main_gui.py` – interfejs graficzny aplikacji
- `caesar.py`, `vigenere.py`, `hill.py` – implementacje szyfrów
- `caesar_frequency_attack.py` – analiza częstości dla Cezara
- `kasiski.py` – klasa ataku Kasiski dla szyfru Vigenère’a
- `dictionary.py` – funkcje ładowania i sprawdzania słów
- `utils.py` – funkcje pomocnicze (np. is_english_word, clean_text)
- `english_words.txt` - plik tekstowy zawierający słowa z języka angielskiego

# Autor
Bartłomiej Żochowski

# Licencja
MIT License
