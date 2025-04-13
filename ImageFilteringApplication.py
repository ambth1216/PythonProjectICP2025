'''
Team: Pixel Masters
Members: Indranil, Anuj mishra, Sahil Anand, Rohan, Himanshu
Required labraries:
pillow==10.4.0 
opencv-python==4.11.0.86
numpy==2.1.1
tkinter (standard library)
os (standard library)
'''
from tkinter import *
from tkinter import filedialog, simpledialog, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont
import numpy as np
from os import path
import cv2

class ImageFilterApp:
    def __init__(self,root):
        #Window title, size and position
        self.root = root
        self.root.title("Image Filter")
        self.root.geometry("600x500+100+100")
        self.root.minsize(400,400)

        #Variables
        self.arr_image = None      # NumPy array image
        self.gaussian_blur = None
        self.grayscale_arr = None
        self.edge_arr = None
        self.original_image = None # Pillow image object
        self.working_image = None  # Image on which filters are being applied
        self.display_image = None  # Scaled up image
        self.scale_factor = 1.0
        self.file_path = None
        self.text_can = None

        # Crop variables
        self.crop_mode = False
        self.crop_start_x = None
        self.crop_start_y = None
        self.crop_end_x = None
        self.crop_end_y = None
        self.crop_rectangle = None

        # Text variables
        self.canvas_x = None
        self.canvas_y = None
        self.text = None
        self.font = None
        self.text_color = None

        #Menu and menubar
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        file_menu = Menu(self.menubar, tearoff=False)
        file_menu.add_command(label='Open', command=self.open_image)
        file_menu.add_command(label='Save', command=self.save_image)

        other_menu = Menu(self.menubar, tearoff=False)
        other_menu.add_command(label='About Image', command=self.image_info)
        other_menu.add_command(label='Exit', command= lambda: self.root.quit())

        self.menubar.add_cascade(label='File', menu=file_menu)
        self.menubar.add_cascade(label='Other', menu=other_menu)

        #Frames
        self.buttons_frame = Frame(root)
        self.buttons_frame.pack(side=TOP, fill=X, padx=10, pady=10)

        self.image_frame = Frame(root)
        self.image_frame.pack(expand=True, fill=BOTH, padx=10, pady=10)  

        self.status_frame = Frame(root)
        self.status_frame.pack(side=BOTTOM, fill=X, padx=10, pady=10) 

        # Image informtion toplevel
        self.tp = None

        #Crop buttons
        self.crop_button = Button(self.buttons_frame, text="Crop", state=DISABLED, command=self.toggle_crop_mode)
        self.crop_button.pack(side=LEFT, padx=4)
        self.apply_crop_button = Button(self.buttons_frame, text='Apply Crop', state=DISABLED, command=self.apply_crop)
        self.apply_crop_button.pack(side=LEFT, padx=4)

        #Text on image button
        self.image_text_button = Button(self.buttons_frame, text="Apply Text", state=DISABLED, command=self.add_text)
        self.image_text_button.pack(side=LEFT, padx=4)

        # Blur button
        self.blur_button = Button(self.buttons_frame, text="Blur", state=DISABLED, command=self.add_blur)
        self.blur_button.pack(side=LEFT, padx=4)

        #GrayScale button
        self.gray_scale_button = Button(self.buttons_frame, text="Grayscale", state=DISABLED, command=self.add_grayscale)
        self.gray_scale_button.pack(side=LEFT, padx=4)

        #Edge detection button 
        self.edge_button = Button(self.buttons_frame, text='Edge', state=DISABLED, command=self.detect_edge)
        self.edge_button.pack(side=LEFT, padx=4)

        # Image rotate button
        self.rotate_button = Button(self.buttons_frame, text="Rotate", state=DISABLED, command=self.rot_img)
        self.rotate_button.pack(side=LEFT, padx=5)

        # Image flip button
        self.flip_button = Button(self.buttons_frame, text='Flip', state=DISABLED, command=self.flip)
        self.flip_button.pack(side=LEFT, padx=5)

        #Reset button
        self.reset_button = Button(self.buttons_frame, text='Reset', state=DISABLED, command=self.reset_image_to_original)
        self.reset_button.pack(side=LEFT, padx=4)

        #Image Canvas
        self.canvas = Canvas(self.image_frame, bg='white')
        self.canvas.pack(expand=True, fill=BOTH)

        #Statusbar label
        self.status_label = Label(self.status_frame, text='Open an Image')
        self.status_label.pack(side=LEFT, padx=4)

        # Functions to bind on canvas when certain mouse actions are performed(defined for left mouse button)
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_released)

    def open_image(self):
        self.file_path = filedialog.askopenfilename(title="Open", initialdir='/',
                    filetypes=[('Image files', '*.png *.jpg *.bmp *.webp *.jpeg')]
                )
        if self.file_path:
            try:
                self.original_image = Image.open(self.file_path)
                self.reset_image_to_original()
                self.status_label.config(text='Ready to filter image')

                self.crop_button.config(state=NORMAL)
                self.image_text_button.config(state=NORMAL)
                self.blur_button.configure(state=NORMAL)
                self.gray_scale_button.config(state=NORMAL)
                self.edge_button.config(state=NORMAL)
                self.rotate_button.config(state=NORMAL)
                self.flip_button.config(state=NORMAL)
                self.reset_button.config(state=NORMAL)
            except Exception as e:
                self.status_label.config(text=f'Error {str(e)}')
            
    def reset_image_to_original(self):
        if self.original_image:
            self.working_image = self.original_image.copy()
            self.update_canvas()
            self.status_label.config(text='Reset to original image...')
    
    def update_canvas(self):
        if self.working_image:
            #clearing canvas
            self.canvas.delete('all')

            # Get canvas width and height
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            # if canvas has not been initilised
            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width = self.image_frame.winfo_width() or 600    # minimum window width
                canvas_height = self.image_frame.winfo_height() or 400  # minimum window height
            
            img_width, img_height = self.working_image.size # get image width & height using size method of pillow
            
            # Calculate the scaling factor
            width_ratio = canvas_width/img_width
            height_ratio = canvas_height/img_height
            self.scale_factor = min(width_ratio, height_ratio)
            
            new_width = int(img_width * self.scale_factor)
            new_height = int(img_height * self.scale_factor)
            
            # Resize the image
            resized_image = self.working_image.resize((new_width, new_height), Image.LANCZOS)  # lanczos is a resampling filter which enchance the inage quality when the image is scaled up 
            
            # Convert to PhotoImage
            self.display_image = ImageTk.PhotoImage(resized_image)
            
            # Calculate position to center the image
            x_pos = (canvas_width - new_width) // 2
            y_pos = (canvas_height - new_height) // 2

            self.image_coordinates = (x_pos, y_pos)
            self.image_dimensions = (img_width, img_height)
            
            # Add image to canvas
            self.canvas.create_image(x_pos, y_pos, anchor='nw', image=self.display_image)
            
    def image_info(self):
        if self.display_image:
            self.tp = Toplevel(self.root)
            self.tp.title('Image Info')
            self.tp.geometry('500x350')
            self.tp.resizable(False,False)

            img_height,img_width = self.original_image.size
            img_mode = self.original_image.mode
            img_formate = self.original_image.format
            img_dis = self.original_image.format_description
            img_name = self.original_image.filename
            self.numpy_opreations()
            var =  f'{self.arr_image.shape}'

            tplbel1 = Label(self.tp,text=f'Dimensions: {img_width}x{img_height} pixels')
            tplbel1.pack(pady=4)
            tplbel2 = Label(self.tp,text=f'Mode: {img_mode}')
            tplbel2.pack(pady=10)
            tplbel3 = Label(self.tp,text=f'Format: {img_formate}')
            tplbel3.pack(pady=10)
            tplbel4 = Label(self.tp,text=f'Format discription: {img_dis}')
            tplbel4.pack(pady=10)
            tplbel5 = Label(self.tp,text=f'Image path: {img_name}')
            tplbel5.pack(pady=10, ipady=5)
            tplbel6 = Label(self.tp,text=f'Numpy array image shape: {var}')
            tplbel6.pack(pady=10)

            self.tp.mainloop()
        else:
            self.status_label.config(text='Please open an image')
    
    def save_image(self):
        if self.working_image:
            original_filename = path.basename(self.file_path)
            image_name, image_extension =  path.splitext(original_filename)

            save_file_name = f'{image_name}_modified{image_extension}'
            
            save_path = filedialog.asksaveasfilename(
                initialdir='/',
                initialfile=save_file_name,
                defaultextension= image_extension,
                filetypes=[
                    ("JPEG files", "*.jpg *.jpeg"),
                    ("PNG files", "*.png"),
                    ("BMP files", "*.bmp"),
                    ("All files", "*.*")]
            )
            if save_path:
                try:
                    # Siving the image. The image on which filtering has been done tht is being saved
                    self.working_image.save(save_path)
                    # self.update_canvas()
                    self.status_label.config(text=f"Image saved successfully: {save_path}")
                except Exception as e:
                    self.status_label.config(text=f"Error saving image: {str(e)}")

    def numpy_opreations(self):
        self.arr_image = np.asarray(self.working_image)
    
    def toggle_crop_mode(self):
        if self.working_image:
            self.crop_mode = not self.crop_mode
            
            if self.crop_mode:
                self.crop_button.config(relief=SUNKEN)
                self.status_label.config(text="Crop Mode: Select area to crop")
                # Clear any existing crop rectangle
                if self.crop_rectangle:
                    self.canvas.delete(self.crop_rectangle)
                    self.crop_rectangle = None
                self.apply_crop_button.config(state=DISABLED)
            else:
                self.crop_button.config(relief=RAISED)
                self.status_label.config(text="Crop Mode disabled")
                # Clear any existing crop rectangle
                if self.crop_rectangle:
                    self.canvas.delete(self.crop_rectangle)
                    self.crop_rectangle = None
                self.apply_crop_button.config(state=DISABLED)
    
    def on_mouse_press(self, event):
        if self.crop_mode and self.working_image:
            # Store the starting position
            self.crop_start_x = event.x
            self.crop_start_y = event.y
            
            # Clear any existing rectangle
            if self.crop_rectangle:
                self.canvas.delete(self.crop_rectangle)
                self.crop_rectangle = None
    
    def on_mouse_motion(self, event):
        if self.crop_mode and self.working_image and self.crop_start_x is not None:
            # Update end position
            self.crop_end_x = event.x
            self.crop_end_y = event.y
            
            # Redraw the rectangle
            if self.crop_rectangle:
                self.canvas.delete(self.crop_rectangle)
            
            self.crop_rectangle = self.canvas.create_rectangle(
                self.crop_start_x, self.crop_start_y, 
                self.crop_end_x, self.crop_end_y,
                outline="white", width=2
            )
    
    def on_mouse_released(self, event):
        if self.crop_mode and self.working_image and self.crop_start_x is not None:
            # Finalize end position
            self.crop_end_x = event.x
            self.crop_end_y = event.y
            
            # Checking a valid selection
            if (abs(self.crop_end_x - self.crop_start_x) > 10 and 
                abs(self.crop_end_y - self.crop_start_y) > 10):
                self.apply_crop_button.config(state=NORMAL)
                self.status_label.config(text="Crop area selected. Click 'Apply Crop' to crop.")
            else:
                if self.crop_rectangle:
                    self.canvas.delete(self.crop_rectangle)
                    self.crop_rectangle = None
                self.apply_crop_button.config(state=DISABLED)
                self.status_label.config(text="Selection too small. Try again.")
    
    def apply_crop(self):
        if (self.working_image and self.crop_rectangle and 
            self.crop_start_x is not None and self.crop_end_x is not None):
            
            # Get image position and size from canvas
            img_x, img_y = self.image_coordinates
            
            # Convert canvas coordinates to image coordinates
            start_x = max(0, (self.crop_start_x - img_x) / self.scale_factor)
            start_y = max(0, (self.crop_start_y - img_y) / self.scale_factor)
            end_x = min(self.working_image.width, (self.crop_end_x - img_x) / self.scale_factor)
            end_y = min(self.working_image.height, (self.crop_end_y - img_y) / self.scale_factor)
            
            # Ensure start is less than end
            if start_x > end_x:
                start_x, end_x = end_x, start_x
            if start_y > end_y:
                start_y, end_y = end_y, start_y
            
            start_x, start_y = int(start_x), int(start_y)
            end_x, end_y = int(end_x), int(end_y)
            
            # Crop the image using numpy slicing method
            self.numpy_opreations()
            self.crop_arr_image = self.arr_image[start_y:end_y,start_x:end_x]
            self.working_image = Image.fromarray(self.crop_arr_image)
            
            # Clear crop rectangle
            if self.crop_rectangle:
                self.canvas.delete(self.crop_rectangle)
                self.crop_rectangle = None
            
            # Exit crop mode
            self.crop_mode = False
            self.crop_button.config(relief=RAISED)
            self.apply_crop_button.config(state=DISABLED)
            
            # The crop image will be resize according to canvas dimensions
            self.update_canvas()
            self.status_label.config(text="Image cropped successfully")

    def image_drawing(self):
        if self.working_image:
            draw = ImageDraw.Draw(self.working_image)

            img_x, img_y = self.image_coordinates
            text_x = max(0, (self.canvas_x - img_x) / self.scale_factor)
            text_y = max(0, (self.canvas_y - img_y) / self.scale_factor)
            text_position = (text_x, text_y)

            draw.text(text_position, self.text, fill=self.text_color, font=self.font)

    def add_text(self):
        if self.working_image:
    
            self.text = simpledialog.askstring("Add Text", "Enter text to add:")

            if self.text:
                fontsize = simpledialog.askinteger('Fontsize', 'Enter font size', initialvalue=24)
                self.font = ImageFont.truetype("arial.ttf", fontsize)
                if fontsize:
                    color_choosed = colorchooser.askcolor(title='Select colour') # The colorchooser return the vale in the form of list 
                    # like ((rbg), hexadecimal value). we have choosen hexadecimal value which has index number 1
                    self.text_color = color_choosed[0]
                    canvas_text_color = color_choosed[1]
                    self.status_label.config(text='Click on image where you want to place the text.')

                    def place_text(event):
                        self.canvas_x = self.canvas.canvasx(event.x)
                        self.canvas_y = self.canvas.canvasy(event.y)
                
                        self.canvas.create_text(self.canvas_x, self.canvas_y, text=self.text, fill=canvas_text_color, font=("Arial", fontsize))
                        self.image_drawing()
                        self.canvas.unbind("<Button-1>")
                        self.canvas.config(cursor='arrow') 

                    self.canvas.config(cursor='plus')    
                    self.canvas.unbind("<ButtonPress-1>")
                    self.canvas.bind("<Button-1>", place_text)
                    self.status_label.config(text=f'{self.text} added')           
        else:
            self.status_label.config(text='Please open an image.')

    def add_blur(self):
        if self.working_image:
            self.numpy_opreations()
            self.gaussian_blur = self.arr_image
            # Gaussian Blur
            self.gaussian_blur = cv2.GaussianBlur(self.gaussian_blur, (5, 5), 0)  # Kernel size 5x5, Std deviation 0
            self.working_image = Image.fromarray(self.gaussian_blur)
            self.update_canvas()
            self.status_label.config(text="Applied blur filter")
            
            # self.working_image = self.working_image.filter(ImageFilter.GaussianBlur(radius=1))
            # self.update_canvas()
            # self.status_label.config(text="Applied blur filter")

    def add_grayscale(self):
        self.numpy_opreations()
        self.grayscale_arr = self.arr_image
        image_bgr = cv2.cvtColor(self.grayscale_arr, cv2.COLOR_RGB2BGR)
        self.grayscale_arr = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

        self.working_image = Image.fromarray(self.grayscale_arr)
        self.update_canvas()
        self.status_label.config(text="Applied grayscale filter")

    def detect_edge(self):
        self.numpy_opreations()
        self.edge_arr = self.arr_image
        edge = cv2.Canny(self.edge_arr, 50, 150)
        self.working_image = Image.fromarray(edge)

        self.update_canvas() 
        self.status_label.config(text="Edge detected")

    def rot_img(self):
        if self.working_image:
            self.numpy_opreations()
            self.arr_image = np.rot90(self.arr_image)

            self.working_image = Image.fromarray(self.arr_image)
            self.update_canvas()
            self.status_label.config(text='Image rotated')

    def flip_image(self):
        if self.working_image:
            self.working_image = cv2.flip(self.working_image, 0) # 0 is the flip tag means flipping image vertically
            self.update_canvas()
            self.status_label.config(text='Image flipped')               

# resize the image of the canvas when the window is configured i.e when window is maximised or its size is changed
# the below function recalculate the image scale factor 
def window_resize(event):
    if hasattr(app, 'display_image') and app.display_image:
        app.update_canvas()


if __name__ == '__main__':
    root = Tk()
    app = ImageFilterApp(root)

    root.bind('<Configure>', window_resize)

    root.mainloop()

