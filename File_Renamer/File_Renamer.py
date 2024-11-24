import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.ttk import Progressbar

# pyinstaller --onefile --noconsole --add-data "C:\Users\<User>\AppData\Local\Programs\Python\Python311\Lib\site-packages\tkinter;tkinter" your_script_name.py

def browse_source():
    folder = filedialog.askdirectory()
    if folder:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, folder)

def browse_dest():
    folder = filedialog.askdirectory()
    if folder:
        dest_entry.delete(0, tk.END)
        dest_entry.insert(0, folder)

def rename_files():
    source_folder = source_entry.get()
    dest_folder = dest_entry.get()
    new_name_base = name_entry.get()
    start_number_str = number_entry.get()

    if not all([source_folder, dest_folder, new_name_base, start_number_str]):
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        start_number = int(start_number_str)
    except ValueError:
        messagebox.showerror("Error", "Invalid starting number. Please enter an integer.")
        return

    if not os.path.isdir(source_folder):
        messagebox.showerror("Error", f"Source folder not found: {source_folder}")
        return

    if not os.path.isdir(dest_folder):  # Check destination folder exists
        try:
            os.makedirs(dest_folder) #Create if doesn't exists
        except Exception as e:
            messagebox.showerror("Error", f"Could not create destination folder: {e}")
            return


    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    total_files = len(files)

    if total_files == 0:
        messagebox.showinfo("Info", "No files found in the source folder.")
        return


    for i, filename in enumerate(files):
        try:
            new_filename = f"{new_name_base}{start_number + i}{os.path.splitext(filename)[1]}"
            source_path = os.path.join(source_folder, filename)
            dest_path = os.path.join(dest_folder, new_filename)
            os.rename(source_path, dest_path)

            progress_bar["value"] = (i + 1) / total_files * 100
            root.update_idletasks()

        except Exception as e:  # Handle file rename errors
            messagebox.showerror("Error", f"An error occurred while renaming {filename}: {e}")
            return

    messagebox.showinfo("Success", f"Successfully renamed {total_files} files.")



root = tk.Tk()
root.title("File Renamer")

source_label = tk.Label(root, text="Source Folder:")
source_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
source_entry = tk.Entry(root, width=40)
source_entry.grid(row=0, column=1, padx=5, pady=5)
source_button = tk.Button(root, text="Browse", command=browse_source)
source_button.grid(row=0, column=2, padx=5, pady=5)


dest_label = tk.Label(root, text="Destination Folder:")
dest_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
dest_entry = tk.Entry(root, width=40)
dest_entry.grid(row=1, column=1, padx=5, pady=5)
dest_button = tk.Button(root, text="Browse", command=browse_dest)
dest_button.grid(row=1, column=2, padx=5, pady=5)

name_label = tk.Label(root, text="New File Name:")
name_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
name_entry = tk.Entry(root, width=40)
name_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=2)

number_label = tk.Label(root, text="Starting Number:")
number_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
number_entry = tk.Entry(root, width=10)
number_entry.grid(row=3, column=1, padx=5, pady=5)

progress_bar = Progressbar(root, length=300, mode="determinate")
progress_bar.grid(row=4, column=0, columnspan=3, padx=5, pady=10)

rename_button = tk.Button(root, text="Rename Files", command=rename_files)
rename_button.grid(row=5, column=0, columnspan=3, pady=10)

root.mainloop()