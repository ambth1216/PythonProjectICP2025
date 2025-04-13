from tkinter import *
from tkinter import filedialog,simpledialog
from PIL import Image, ImageTk
import numpy as np

class ImageFilterApp:
    def __init__(self,root):
        self.root = root
        self.root.title("Image Filter")
        self.root.geometry("500x500+100+100")
        self.root.minsize(400,400)

        self.var = StringVar()
        self.text_to_add = []
        self.original_image = None
        self.display_image = None
        self.arr_img = np.asarray(self.original_image)
        self.scale_factor = 1.0
        self.txt_tp = None

        #Crop variables
        self.text_mode = False
        # self.text_x = 0
        # self.text_y = None
        self.text_can = None

        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        file_menu = Menu(self.menubar, tearoff=False)
        file_menu.add_command(label='Open', command=self.open_image)

        self.menubar.add_cascade(label='File', menu=file_menu)

        #Frames
        self.buttons_frame = Frame(root)
        self.buttons_frame.pack(side=TOP, fill=X, padx=10, pady=10)


        self.image_frame = Frame(root)
        self.image_frame.pack(expand=True, fill=BOTH, padx=10, pady=10)  

        self.status_frame = Frame(root)
        self.status_frame.pack(side=BOTTOM, fill=X, padx=10, pady=10) 

        #Text buttons
        self.text_button = Button(self.buttons_frame, text="Add Text", state=DISABLED, command=self.toogle_text_mode)
        self.text_button.pack(side=LEFT, padx=4)
        # self.apply_text_button = Button(self.buttons_frame, text='Apply Text', state=DISABLED, command=self.apply_text)
        # self.apply_text_button.pack(side=LEFT, padx=4)

        #Reset button
        self.reset_button = Button(self.buttons_frame, text='Reset', state=DISABLED, command=self.reset_image_to_original)
        self.reset_button.pack(side=LEFT, padx=4)

        #Canvas bind functionalities
        
        # self.canvas.bind("<ButtonRelease-1>", self.mouse_up_for_text)

        #Image Canvas
        self.canvas = Canvas(self.image_frame, bg='white')
        self.canvas.pack(expand=True, fill=BOTH)

        #Statusbar label
        self.status_label = Label(self.status_frame, text='Open an Image')
        self.status_label.pack(side=LEFT, padx=4)


    def open_image(self):
        file_path = filedialog.askopenfilename(title="Open", initialdir='/',
                    filetypes=[('Image files', '*.png *.jpg *.bmp *.webp *.jpeg')]
                )
        if file_path:
            try:
                self.original_image = Image.open(file_path)

                self.text_button.config(state=NORMAL)
                self.reset_button.config(state=NORMAL)
            except Exception as e:
                self.status_label.config(text=f'Error {str(e)}')
            self.update_canvas()
    
    def update_canvas(self):
        if self.original_image:
            self.canvas.delete('all')

            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width = self.image_frame.winfo_width() or 600    
                canvas_height = self.image_frame.winfo_height() or 400  
            
            img_width, img_height = self.original_image.size 
            
            width_ratio = canvas_width/img_width
            height_ratio = canvas_height/img_height
            self.scale_factor = min(width_ratio, height_ratio)
            
            new_width = int(img_width * self.scale_factor)
            new_height = int(img_height * self.scale_factor)
            
            resized_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)  # lanczos is a resampling filter which enchance the inage quality when the image is scaled up 
            
            self.display_image = ImageTk.PhotoImage(resized_image)
            
            x_pos = (canvas_width - new_width) // 2
            y_pos = (canvas_height - new_height) // 2
            
            self.canvas.create_image(x_pos, y_pos, anchor='nw', image=self.display_image)
            
    def reset_image_to_original(self):
        if self.display_image:
            self.display_image = self.original_image.copy()
            self.update_canvas()
            self.status_label.config(text='Reset to original image...')

    def toogle_text_mode(self):
        if self.display_image:
            self.text_mode = not self.text_mode

            if self.text_mode:
                self.text_button.config(relief=SUNKEN)
                self.canvas.config(cursor='plus')
                # text_display = simpledialog.askstring('Add text', 'Enter text to add: ')
                # if text_display:
                #     def place_text(event):
                #         text_x = event.x
                #         text_y = event.y
                #         self.text_can = self.canvas.create_text(text_x, text_y, text=text_display, font=(30), fill='black')
                #         self.text_button.config(relief=RAISED)
                #         self.text_mode = False
                #         self.canvas.config(cursor='arrow')
                #         self.canvas.unbind('<Button-1>')

                # self.canvas.unbind("<ButtonRelease-1>")
                self.canvas.bind("<Button-1>", self.apply_text)
                # self.text_mode = False
            # self.apply_text_button.config(state=DISABLED)
            else:
                self.text_button.config(relief=RAISED)
                self.canvas.config(cursor='arrow')
                self.canvas.unbind("<Button-1>")
                self.status_label.config(text='Add text mode disable')
                # if self.text_can:
                #     self.canvas.delete(self.text_can)
                #     self.text_can = None
                # self.apply_text_button.config(state=DISABLED)
            # self.add_text()
    
   
    # def text_toplevel(self):

    #     if self.text_mode == True:
    #         self.txt_tp = Toplevel()
    #         self.txt_tp.title('Add Text')
    #         self.txt_tp.geometry('500x90')
    #         self.txt_tp.resizable(False,False)
    #         txt_frame = Frame(self.txt_tp)
    #         txt_frame.pack(side=TOP,fill=X)
    #         textbox = Entry(txt_frame, font=(15), textvariable=self.var)
    #         textbox.pack(side=LEFT)
    #         apply_text_button = Button(txt_frame, text='Apply text', command=self.apply_text)
    #         apply_text_button.pack(side=LEFT, padx=5)

    def apply_text(self, event):
        text_x = event.x
        text_y = event.y
        
        text_display = simpledialog.askstring('Add text', 'Enter text to add: ')
        if text_display:
            print(text_x,text_y)
            self.canvas.create_text(text_x, text_y, text=text_display, font=(30), fill='black')
            self.text_button.config(relief=RAISED)
            self.text_mode = False
            self.canvas.config(cursor='arrow')
            self.canvas.unbind('<Button-1>')
        else:
            self.status_label.config(text='Select a text')
            self.text_button.config(relief=RAISED)
            self.text_mode = False

    # def add_text(self):
    #     if not self.display_image:
    #         return
        
        
    #     text = simpledialog.askstring("Add Text", "Enter text to add:")

    #     if text:
    #         fontsize = simpledialog.askinteger('Fontsize', 'Enter font size', initialvalue=24)
                    
    #         def place_text(event):
    #             canvas_x = self.canvas.canvasx(event.x)
    #             canvas_y = self.canvas.canvasy(event.y)
    #             self.text_can = self.canvas.create_text(canvas_x,canvas_y, text=f'{text}', font=(fontsize),fill='black')
    #             self.canvas.unbind("<Button-1>")
                    
    #         self.canvas.unbind("<ButtonPress-1>")
    #         self.canvas.bind("<Button-1>", place_text)
        
             
def window_resize(event):
    if hasattr(app, 'display_image') and app.display_image:
        app.update_canvas()


if __name__ == '__main__':
    root = Tk()

    app = ImageFilterApp(root)

    root.bind('<Configure>', window_resize)

    root.mainloop()

