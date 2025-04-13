import tkinter as tk
from tkinter import ttk, filedialog, simpledialog

class ImageFilterApplication:
    def __init__(self,root):
        self.root = root
        self.root.title('Image filter app')
        self.root.geometry('500x500')
        self.root.minsize(40,400)

        self.buttons_frame = ttk.Frame(self.root)
        self.buttons_frame.pack(side=tk.LEFT, fill=tk.X)

if __name__ == "__main__":

    root = tk.Tk()

    app = ImageFilterApplication(root)