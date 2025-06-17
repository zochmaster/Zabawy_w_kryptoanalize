import tkinter as tk
from tkinter import messagebox
import random
from caesar import caesar_encrypt, caesar_decrypt
from vigenere import (
    vigenere_encrypt,
    vigenere_decrypt,
    vigenere_kasiski_attack,
    vigenere_brute_force_attack
)
from hill import hill_encrypt, hill_decrypt, hill_brute_force_attack, is_invertible_matrix, preserve_non_letters
from dictionary import load_dictionary
from caesar_frequency_attack import caesar_frequency_attack


# Główne okno aplikacji GUI zbudowane w Tkinter
window = tk.Tk()
window.title("Classic Ciphers GUI")
window.geometry("800x700")

# Wczytanie słownika do pamięci (używany do walidacji odszyfrowań)
dictionary = load_dictionary()

# Zmienne kontrolne do wyboru szyfru, metody ataku i rozmiaru macierzy Hilla
cipher_var = tk.StringVar(value="vigenere")
attack_method_var = tk.StringVar(value="auto")
matrix_size_var = tk.StringVar(value="2x2")

# Lista pól wejściowych reprezentujących macierz szyfru Hilla
hill_matrix_entries = []

# Elementy GUI – wybór typu szyfru
tk.Label(window, text="Cipher Type").pack()
cipher_menu = tk.OptionMenu(window, cipher_var, "caesar", "vigenere", "hill")
cipher_menu.pack()

# Wybór metody ataku (dynamicznie zmieniany w zależności od szyfru)
attack_menu_label = tk.Label(window, text="Attack Method")
attack_menu_label.pack()
attack_menu = tk.OptionMenu(window, attack_method_var, "auto", "kasiski", "brute-force", "frequency")
attack_menu.pack()

# Pole do wprowadzania tekstu (szyfrogramu lub jawnego)
tk.Label(window, text="Input Text").pack()
text_entry = tk.Text(window, height=10, width=80)
text_entry.pack()

# Sekcja klucza / macierzy (zależna od wybranego szyfru)
key_frame = tk.Frame(window)
key_frame.pack()

tk.Label(key_frame, text="Key").grid(row=0, column=0, columnspan=3)
key_entry = tk.Entry(key_frame, width=50)
key_entry.grid(row=1, column=0, columnspan=3)

matrix_size_menu = tk.OptionMenu(key_frame, matrix_size_var, "2x2", "3x3")
hill_matrix_frame = tk.Frame(key_frame)

# Pole wyjściowe z odszyfrowanym/szyfrowanym tekstem
tk.Label(window, text="Output").pack()
output_text = tk.Text(window, height=15, width=80)
output_text.pack()

# Funkcja pomocnicza – odwrotność modulo m
def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# Generuje losową, odwracalną macierz do szyfru Hilla
def generate_valid_matrix(size):
    attempts = 0
    while attempts < 1000:
        matrix = [random.randint(0, 25) for _ in range(size * size)]
        if is_invertible_matrix(matrix, size):
            return matrix
        attempts += 1
    raise ValueError("Nie udało się wygenerować odwracalnej macierzy.")

# Aktualizuje pola do wprowadzania macierzy Hilla
def update_matrix_inputs():
    for widget in hill_matrix_frame.winfo_children():
        widget.destroy()
    hill_matrix_entries.clear()

    size = int(matrix_size_var.get()[0])
    try:
        matrix = generate_valid_matrix(size)
    except ValueError:
        messagebox.showerror("Error", "Nie udało się wylosować poprawnej macierzy.")
        return

    for i in range(size):
        row = []
        for j in range(size):
            entry = tk.Entry(hill_matrix_frame, width=5)
            entry.grid(row=i, column=j, padx=2, pady=2)
            entry.insert(0, str(matrix[i * size + j]))
            row.append(entry)
        hill_matrix_entries.append(row)

    hill_matrix_frame.grid(row=2, column=0, columnspan=3)

# Wyświetla okienko pomocy dla szyfru Hilla
def show_hill_info():
    msg = (
        "Szyfr Hilla używa macierzy klucza do szyfrowania bloków liter.\n\n"
        "Wybierz rozmiar macierzy (2x2 lub 3x3) i wpisz liczby z zakresu 0–25.\n"
        "Macierz musi być odwracalna modulo 26, aby możliwe było deszyfrowanie."
    )
    messagebox.showinfo("Szyfr Hilla — pomoc", msg)

# Aktualizuje listę dostępnych metod ataku w zależności od wybranego szyfru
def update_attack_menu(*args):
    method_menu = attack_menu['menu']
    method_menu.delete(0, 'end')
    c = cipher_var.get()
    if c == 'vigenere':
        options = ["auto", "kasiski", "brute-force"]
    elif c == 'caesar':
        options = ["brute-force", "frequency"]
    else:
        options = ["brute-force"]

    for opt in options:
        method_menu.add_command(label=opt, command=tk._setit(attack_method_var, opt))
    attack_method_var.set(options[0])

    if c == 'hill':
        key_entry.grid_remove()
        matrix_size_menu.grid(row=1, column=0)
        tk.Button(key_frame, text="Set Matrix", command=update_matrix_inputs).grid(row=1, column=1)
        tk.Button(key_frame, text="?", command=show_hill_info).grid(row=1, column=2)
        hill_matrix_frame.grid(row=2, column=0, columnspan=3)
    else:
        matrix_size_menu.grid_remove()
        for widget in key_frame.grid_slaves():
            if isinstance(widget, tk.Button):
                widget.grid_remove()
        key_entry.grid(row=1, column=0, columnspan=3)
        hill_matrix_frame.grid_forget()

cipher_var.trace("w", update_attack_menu)
update_attack_menu()

# Obsługa przycisku "Encrypt"
def run_encrypt():
    text = text_entry.get("1.0", "end").strip()
    cipher_type = cipher_var.get()

    if not text:
        messagebox.showerror("Error", "Wprowadź tekst wejściowy.")
        return

    try:
        if cipher_type == "caesar":
            key = int(key_entry.get().strip())
            result = caesar_encrypt(text, key)
        elif cipher_type == "vigenere":
            key = key_entry.get().strip()
            result = vigenere_encrypt(text, key)
        elif cipher_type == "hill":
            size = int(matrix_size_var.get()[0])
            key_numbers = []
            if not hill_matrix_entries or not all(row for row in hill_matrix_entries):
                messagebox.showerror("Error", "Najpierw ustaw macierz za pomocą przycisku 'Set Matrix'.")
                return
            for row in hill_matrix_entries:
                for e in row:
                    val_str = e.get().strip()
                    if not val_str.isdigit() or not (0 <= int(val_str) < 26):
                        messagebox.showerror("Error", "Wszystkie pola muszą zawierać liczby całkowite 0–25.")
                        return
                    key_numbers.append(int(val_str))
            if len(key_numbers) != size * size or not is_invertible_matrix(key_numbers, size):
                messagebox.showerror("Error", "Macierz nieprawidłowa lub nieodwracalna.")
                return
            raw = hill_encrypt(text, key_numbers)
            result = preserve_non_letters(text, raw)
        else:
            result = "Nieobsługiwany szyfr."
    except Exception as e:
        result = f"Error: {e}"

    output_text.delete("1.0", "end")
    output_text.insert("1.0", result)

# Obsługa przycisku "Decrypt"
def run_decrypt():
    text = text_entry.get("1.0", "end").strip()
    cipher_type = cipher_var.get()

    if not text:
        messagebox.showerror("Error", "Wprowadź tekst wejściowy.")
        return

    try:
        if cipher_type == "caesar":
            key = int(key_entry.get().strip())
            result = caesar_decrypt(text, key)
        elif cipher_type == "vigenere":
            key = key_entry.get().strip()
            result = vigenere_decrypt(text, key)
        elif cipher_type == "hill":
            size = int(matrix_size_var.get()[0])
            key_numbers = []
            if not hill_matrix_entries or not all(row for row in hill_matrix_entries):
                messagebox.showerror("Error", "Najpierw ustaw macierz za pomocą przycisku 'Set Matrix'.")
                return
            for row in hill_matrix_entries:
                for e in row:
                    val_str = e.get().strip()
                    if not val_str.isdigit() or not (0 <= int(val_str) < 26):
                        messagebox.showerror("Error", "Wszystkie pola muszą zawierać liczby całkowite 0–25.")
                        return
                    key_numbers.append(int(val_str))
            if len(key_numbers) != size * size or not is_invertible_matrix(key_numbers, size):
                messagebox.showerror("Error", "Macierz nieprawidłowa lub nieodwracalna.")
                return
            raw = hill_decrypt(text, key_numbers)
            result = preserve_non_letters(text, raw)
        else:
            result = "Nieobsługiwany szyfr."
    except Exception as e:
        result = f"Error: {e}"

    output_text.delete("1.0", "end")
    output_text.insert("1.0", result)

# Obsługa przycisku "Attack"
def run_attack():
    text = text_entry.get("1.0", "end").strip().upper()
    cipher_type = cipher_var.get()
    method = attack_method_var.get()

    if not text:
        messagebox.showerror("Błąd", "Wprowadź tekst wejściowy.")
        return

    try:
        if cipher_type == "hill":
            if method != "brute-force":
                messagebox.showerror("Błąd", "Dla szyfru Hilla dostępny jest tylko brute-force.")
                result = "Niepoprawna metoda ataku."
            else:
                size = int(matrix_size_var.get()[0])
                result = hill_brute_force_attack(text, dictionary, top_n=5, size=size)
        elif cipher_type == "caesar":
            if method == "brute-force":
                result = "\n".join(f"{k}: {caesar_decrypt(text, k)}" for k in range(26))
            elif method == "frequency":
                result = caesar_frequency_attack(text, dictionary)
        elif cipher_type == "vigenere":
            if method == "auto":
                results = vigenere_kasiski_attack(text, dictionary)
                if results:
                    result = "\n\n".join([f"Klucz (Kasiski): {k}\nOdszyfrowany tekst:\n{t}" for k, t in results])
                else:
                    key, decrypted = vigenere_brute_force_attack(text, dictionary)
                    if key:
                        result = f"Klucz (brute-force): {key}\nOdszyfrowany tekst:\n{decrypted}"
                    else:
                        result = "Nie udało się złamać szyfru ani metodą Kasiski, ani brute-force."
            elif method == "kasiski":
                results = vigenere_kasiski_attack(text, dictionary)
                if results:
                    result = "\n\n".join([f"Klucz: {k}\nOdszyfrowany tekst:\n{t}" for k, t in results])
                else:
                    result = "Nie udało się złamać szyfru metodą Kasiski."
            elif method == "brute-force":
                key, decrypted = vigenere_brute_force_attack(text, dictionary)
                if key:
                    result = f"Klucz: {key}\nOdszyfrowany tekst:\n{decrypted}"
                else:
                    result = "Nie udało się znaleźć poprawnego klucza metodą brute-force."

    except Exception as e:
        result = f"Błąd: {e}"

    output_text.delete("1.0", "end")
    output_text.insert("1.0", result)

# Przyciski
tk.Button(window, text="Encrypt", command=run_encrypt).pack()
tk.Button(window, text="Decrypt", command=run_decrypt).pack()
tk.Button(window, text="Attack", command=run_attack).pack()

# Uruchomienie aplikacji
window.mainloop()
