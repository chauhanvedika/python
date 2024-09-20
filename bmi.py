import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import json
import os

# Initialize data storage
DATA_FILE = 'bmi_data.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as file:
        json.dump({}, file)

def load_data():
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def save_bmi(name, bmi):
    data = load_data()
    if name not in data:
        data[name] = []
    data[name].append(bmi)
    save_data(data)

def calculate_and_show_bmi():
    name = entry_name.get().strip()
    weight = entry_weight.get().strip()
    height = entry_height.get().strip()
    
    if not name or not weight or not height:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return
    
    try:
        weight = float(weight)
        height = float(height)
        
        if weight <= 0 and height <= 0:
            raise ValueError("Invalid values")
        
        bmi = calculate_bmi(weight, height)
        save_bmi(name, bmi)
        
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obesity"
        
        result_text.set(f"{name}, your BMI is {bmi:.2f}. You are {category}.")
    
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for weight and height.")

def show_history():
    name = entry_name.get().strip()
    
    if not name:
        messagebox.showerror("Input Error", "Please enter a name.")
        return
    
    data = load_data()
    
    if name not in data or not data[name]:
        messagebox.showinfo("No Data", f"No BMI history for {name}.")
        return
    
    history = data[name]
    plt.figure(figsize=(10, 5))
    plt.plot(history, marker='o', linestyle='-', color='b')
    plt.title(f'BMI History for {name}')
    plt.xlabel('Entry')
    plt.ylabel('BMI')
    plt.grid(True)
    plt.show()

# Create the main application window
root = tk.Tk()
root.title("BMI Calculator")

# Create and place widgets
tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Weight (kg):").grid(row=1, column=0, padx=10, pady=5)
entry_weight = tk.Entry(root)
entry_weight.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Height (m):").grid(row=2, column=0, padx=10, pady=5)
entry_height = tk.Entry(root)
entry_height.grid(row=2, column=1, padx=10, pady=5)

result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, wraplength=300, justify='left').grid(row=4, columnspan=2, padx=10, pady=5)

tk.Button(root, text="Calculate BMI", command=calculate_and_show_bmi).grid(row=3, columnspan=2, pady=10)
tk.Button(root, text="Show History", command=show_history).grid(row=5, columnspan=2, pady=10)

# Run the main application loop
root.mainloop()
