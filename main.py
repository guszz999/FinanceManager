import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from datetime import datetime

import matplotlib.pyplot as plt

# File to store data
DATA_FILE = "finance_data.csv"


# Initialize CSV if it doesn't exist
def initialize_csv():
    try:
        with open(DATA_FILE, mode='x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Type", "Amount", "Category", "Description"])
    except FileExistsError:
        pass


# Add a new entry
def add_entry(entry_type):
    def save_entry():
        date = datetime.now().strftime("%Y-%m-%d")
        amount = amount_var.get()
        category = category_var.get()
        description = description_var.get()

        if not amount or not category:
            messagebox.showerror("Input Error", "Amount and Category are required!")
            return

        try:
            amount = float(amount)
            with open(DATA_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([date, entry_type, amount, category, description])
            messagebox.showinfo("Success", f"{entry_type.capitalize()} added successfully!")
            entry_window.destroy()
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a number!")

    # Create entry window
    entry_window = tk.Toplevel(root)
    entry_window.title(f"Add {entry_type.capitalize()}")

    tk.Label(entry_window, text="Amount:").grid(row=0, column=0, padx=10, pady=5)
    amount_var = tk.StringVar()
    tk.Entry(entry_window, textvariable=amount_var).grid(row=0, column=1, padx=10, pady=5)

    tk.Label(entry_window, text="Category:").grid(row=1, column=0, padx=10, pady=5)
    category_var = tk.StringVar()
    tk.Entry(entry_window, textvariable=category_var).grid(row=1, column=1, padx=10, pady=5)

    tk.Label(entry_window, text="Description:").grid(row=2, column=0, padx=10, pady=5)
    description_var = tk.StringVar()
    tk.Entry(entry_window, textvariable=description_var).grid(row=2, column=1, padx=10, pady=5)

    tk.Button(entry_window, text="Save", command=save_entry).grid(row=3, column=0, columnspan=2, pady=10)


# View Summary
def view_summary():
    try:
        with open(DATA_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            income, expenses = 0, 0

            for row in reader:
                _, entry_type, amount, _, _ = row
                amount = float(amount)
                if entry_type == "income":
                    income += amount
                elif entry_type == "expense":
                    expenses += amount

            net_savings = income - expenses
            summary_text = (f"Total Income: ${income:.2f}\n"
                            f"Total Expenses: ${expenses:.2f}\n"
                            f"Net Savings: ${net_savings:.2f}")

            messagebox.showinfo("Summary", summary_text)
    except FileNotFoundError:
        messagebox.showerror("Error", "No data file found. Please add entries first.")


# Visualize Expenses
def visualize_expenses():
    try:
        with open(DATA_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            category_totals = {}

            for row in reader:
                _, entry_type, amount, category, _ = row
                if entry_type == "expense":
                    category_totals[category] = category_totals.get(category, 0) + float(amount)

            if not category_totals:
                messagebox.showinfo("No Data", "No expenses to visualize.")
                return

            categories = list(category_totals.keys())
            totals = list(category_totals.values())

            plt.figure(figsize=(8, 6))
            plt.pie(totals, labels=categories, autopct='%1.1f%%', startangle=140)
            plt.title("Expenses by Category")
            plt.axis('equal')
            plt.show()
    except FileNotFoundError:
        messagebox.showerror("Error", "No data file found. Please add entries first.")


# Main window setup
root = tk.Tk()
root.title("Personal Finance Manager")
root.geometry("400x300")

initialize_csv()

# Add buttons
tk.Button(root, text="Add Income", command=lambda: add_entry("income"), width=20).pack(pady=10)
tk.Button(root, text="Add Expense", command=lambda: add_entry("expense"), width=20).pack(pady=10)
tk.Button(root, text="View Summary", command=view_summary, width=20).pack(pady=10)
tk.Button(root, text="Visualize Expenses", command=visualize_expenses, width=20).pack(pady=10)
tk.Button(root, text="Exit", command=root.quit, width=20).pack(pady=10)

root.mainloop()
    
