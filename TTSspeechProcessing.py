import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from gtts import gTTS
import os
global speech

def speech_generation():
    global speech
    text = var.get()
    language = 'en'
    speech = gTTS(text=text, lang=language, slow=False)

    messagebox.showinfo('Succesfull', 'Speech successfully generated!')

def save_speech():
    save_path = filedialog.asksaveasfilename(
        initialdir='/',
        initialfile='audio',
        defaultextension= '.mp3',
        filetypes=[('MP3 files', '*.mp3')]
    )
    speech.save(save_path)

def play_speech():
    file_path = filedialog.askopenfilename(
        title='Open speech',
        initialdir='/',
        filetypes=[('mp3 files', '*.mp3')]
    )
    os.system(f'start {file_path}')


root = ttk.Window(themename='cyborg')
root.title('TTS')
root.geometry('600x100')
root.resizable(False, False)

var = tk.StringVar()

entry = ttk.Entry(root, textvariable=var, width=20)
entry.pack(side=tk.LEFT, padx=5, expand=1)

speechbutton = ttk.Button(root, text='Generate', command=speech_generation)
speechbutton.pack(side=tk.LEFT, padx=5, expand=1)

savebutton = ttk.Button(root, text='Save', command=save_speech)
savebutton.pack(side=tk.LEFT, padx=5, expand=1)

playbutton = ttk.Button(root, text='Play', command=play_speech)
playbutton.pack(side=tk.LEFT, padx=4, expand=1)


root.mainloop()