import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class FileDeleterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Eliminar Archivos por Fecha")

        # Estilo Material Design
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="white", foreground="black", font=("Arial", 12))
        style.configure("TButton", background="#6200EE", foreground="white", font=("Arial", 12))
        style.map("TButton", background=[("active", "#3700B3")])

        self.setup_ui()

    def setup_ui(self):
        # Etiqueta de selección de carpeta
        self.label_folder = ttk.Label(self.root, text="Carpeta:")
        self.label_folder.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_folder = ttk.Entry(self.root, width=50)
        self.entry_folder.grid(row=0, column=1, padx=10, pady=10)

        self.btn_browse = ttk.Button(self.root, text="Examinar", command=self.browse_folder)
        self.btn_browse.grid(row=0, column=2, padx=10, pady=10)

        # Etiqueta y campo para la fecha
        self.label_date = ttk.Label(self.root, text="Fecha (YYYY-MM-DD):")
        self.label_date.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_date = ttk.Entry(self.root, width=20)
        self.entry_date.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Botón para eliminar archivos
        self.btn_delete = ttk.Button(self.root, text="Eliminar Archivos", command=self.delete_files)
        self.btn_delete.grid(row=2, column=1, pady=20)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry_folder.delete(0, tk.END)
            self.entry_folder.insert(0, folder)

    def delete_files(self):
        folder = self.entry_folder.get()
        date_str = self.entry_date.get()

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Fecha inválida. Use el formato YYYY-MM-DD.")
            return

        if not os.path.isdir(folder):
            messagebox.showerror("Error", "La carpeta no existe.")
            return

        deleted_files = 0
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if mod_time.date() <= date.date():
                    os.remove(file_path)
                    deleted_files += 1

        messagebox.showinfo("Completado", f"Se eliminaron {deleted_files} archivos.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileDeleterApp(root)
    root.mainloop()
