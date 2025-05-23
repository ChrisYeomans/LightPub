import tkinter as tk
import threading
import os
import sys 
from tkinter.ttk import *
from NovelFullBook import NovelFullBook

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.book_entry_label = tk.Label(master, text="Book URL:")
        self.book_entry_label.grid(row=0, column=0, padx=5, pady=5)

        self.book_url_entry = tk.Entry(master, width=65)
        self.book_url_entry.grid(row=1, column=0, padx=5, pady=5)

        self.generateNovelButton = tk.Button(master, text="Generate Novel", width=20, command=self.generate_book)
        self.generateNovelButton.grid(row=1, column=1, padx=5, pady=5)

        self.book_url = tk.StringVar()
        self.book_url.set("")
        self.book_url_entry["textvariable"] = self.book_url

        self.created = tk.Label(master, text="")
        self.created.grid(row=3, column=0, padx=5, pady=5)

    def generate_book(self):
        try:
            book_url = self.book_url.get()
            novelFullBook = NovelFullBook(book_url)
            novelFullBook.set_metadata()
        except Exception as e:
            self.created["text"] = "Error: " + str(e)
            return
        
        threading.Thread(target=self.generate_book_async, args=(novelFullBook,)).start()

    def generate_book_async(self, novelFullBook):
        try:
            self.created['text'] ="Creating E-Book..."
            progress = Progressbar(self.master,
                                        orient=tk.HORIZONTAL, 
                                        length=500, 
                                        mode="determinate",
                                        takefocus=True,
                                        maximum=novelFullBook.num_chapters)
            progress.grid(row=2, column=0, padx=5, pady=5)
            for i in novelFullBook.write_book():
                print(i)
                progress["value"] = i
                self.master.update_idletasks()
            progress["value"] = novelFullBook.num_chapters
            self.created["text"] = "E-Book Created"
        except Exception as e:
            self.created["text"] = "Error: " + str(e)

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


root = tk.Tk()
myapp = App(root)
myapp.master.title("LightPub")
icon = tk.PhotoImage(file = myapp.resource_path("light_pub_icon.png"))
myapp.master.wm_iconphoto(False, icon)
myapp.mainloop()