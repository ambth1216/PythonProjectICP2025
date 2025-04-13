from tkinter import *

class ImageFilterApp:
    def __init__(self,root):
        self.root = root

        self.root.title("Image Filter")
        self.root.geometry("500x400")
        self.root.minsize(400,250)

        # self.root.config(bg="black")

        self.main_menu = Menu(self.root)
        self.main_menu.config(bg="blue")
        self.root.config(menu=self.main_menu)


        f_menu = Menu(self.main_menu)
        f_menu.add_command(label="Browse")
        self.main_menu.add_cascade(label="File", menu=f_menu)


        self.update_label = Label(self.root,text="File")
        self.update_label.pack()

        self.browse_button = Button(self.root,text="Open",command=self.change_label)
        self.browse_button.pack(ipady=0.2)



    def change_label(self):
        self.update_label.config(text="Hello")


if __name__ == "__main__":
    root = Tk()
    app = ImageFilterApp(root)


    root.mainloop()

