import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip


class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")

        # Options for password complexity
        self.length_label = tk.Label(root, text="Password Length:")
        self.length_label.pack()
        self.length_var = tk.IntVar(value=12)
        self.length_entry = tk.Entry(root, textvariable=self.length_var)
        self.length_entry.pack()

        self.include_uppercase_var = tk.BooleanVar(value=True)
        self.include_uppercase_check = tk.Checkbutton(root, text="Include Uppercase Letters",
                                                      variable=self.include_uppercase_var)
        self.include_uppercase_check.pack()

        self.include_numbers_var = tk.BooleanVar(value=True)
        self.include_numbers_check = tk.Checkbutton(root, text="Include Numbers", variable=self.include_numbers_var)
        self.include_numbers_check.pack()

        self.include_special_var = tk.BooleanVar(value=True)
        self.include_special_check = tk.Checkbutton(root, text="Include Special Characters",
                                                    variable=self.include_special_var)
        self.include_special_check.pack()

        self.password_entry = tk.Entry(root, width=40)
        self.password_entry.pack()

        self.generate_button = tk.Button(root, text="Generate Password", command=self.generate_password)
        self.generate_button.pack()

        self.copy_button = tk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack()

    def generate_password(self):
        length = self.length_var.get()
        include_uppercase = self.include_uppercase_var.get()
        include_numbers = self.include_numbers_var.get()
        include_special = self.include_special_var.get()

        if length < 4:
            messagebox.showerror("Error", "Password length should be at least 4")
            return

        characters = string.ascii_lowercase
        if include_uppercase:
            characters += string.ascii_uppercase
        if include_numbers:
            characters += string.digits
        if include_special:
            characters += string.punctuation

        if not characters:
            messagebox.showerror("Error", "No characters available to generate a password")
            return

        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def copy_to_clipboard(self):
        password = self.password_entry.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard")


if __name__ == "__main__":
    root = tk.Tk()
    PasswordGenerator(root)
    root.mainloop()
