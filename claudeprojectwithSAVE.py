import tkinter as tk
from tkinter import filedialog, Button, Label, Frame
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import os
import numpy as np

class ImageFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Filter Application")
        
        # Set window size and position
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Variables
        self.arr_image = None
        self.rotate_arr = None
        self.original_image = None
        self.current_image = None
        self.display_image = None
        self.scale_factor = 1.0
        self.file_path = None
        
        # Crop variables
        self.crop_mode = False
        self.crop_start_x = None
        self.crop_start_y = None
        self.crop_end_x = None
        self.crop_end_y = None
        self.crop_rectangle = None
        
        # Create frames
        self.top_frame = Frame(root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        self.image_frame = Frame(root)
        self.image_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.bottom_frame = Frame(root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        # Browse button
        self.browse_button = Button(self.top_frame, text="Browse Image", command=self.browse_image)
        self.browse_button.pack(side=tk.LEFT, padx=5)
        
        # Filter buttons
        self.blur_button = Button(self.top_frame, text="Blur Filter", command=self.apply_blur, state=tk.DISABLED)
        self.blur_button.pack(side=tk.LEFT, padx=5)
        
        self.sharpen_button = Button(self.top_frame, text="Sharpen Filter", command=self.apply_sharpen, state=tk.DISABLED)
        self.sharpen_button.pack(side=tk.LEFT, padx=5)
        
        self.grayscale_button = Button(self.top_frame, text="Grayscale Filter", command=self.apply_grayscale, state=tk.DISABLED)
        self.grayscale_button.pack(side=tk.LEFT, padx=5)

        self.rotate_button = Button(self.top_frame, text="Rotate", command=self.rot_img, state=tk.DISABLED,)
        self.rotate_button.pack(side=tk.LEFT, padx=5)
        
        # Crop buttons
        self.crop_button = Button(self.top_frame, text="Crop Mode", command=self.toggle_crop_mode, state=tk.DISABLED)
        self.crop_button.pack(side=tk.LEFT, padx=5)
        
        self.apply_crop_button = Button(self.top_frame, text="Apply Crop", command=self.apply_crop, state=tk.DISABLED)
        self.apply_crop_button.pack(side=tk.LEFT, padx=5)
        
        # Save button
        self.save_button = Button(self.top_frame, text="Save Image", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        self.reset_button = Button(self.top_frame, text="Reset Image", command=self.reset_image, state=tk.DISABLED)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Create canvas for image display
        self.canvas = tk.Canvas(self.image_frame, bg="light gray")
        self.canvas.pack(expand=True, fill=tk.BOTH)
        
        # Bind canvas events for crop functionality
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        
        # Status label
        self.status_label = Label(self.bottom_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT)
    
    def browse_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.file_path = file_path
                self.reset_image()
                
                # Enable filter buttons
                self.blur_button.config(state=tk.NORMAL)
                self.sharpen_button.config(state=tk.NORMAL)
                self.grayscale_button.config(state=tk.NORMAL)
                self.rotate_button.config(state=tk.NORMAL)
                self.crop_button.config(state=tk.NORMAL)
                self.reset_button.config(state=tk.NORMAL)
                self.save_button.config(state=tk.NORMAL)
                
                self.status_label.config(text=f"Loaded: {file_path}")
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}")
    
    def reset_image(self):
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.update_display()
            self.status_label.config(text="Image reset to original")
            
            # Reset crop mode
            self.crop_mode = False
            self.crop_button.config(relief=tk.RAISED)
            self.apply_crop_button.config(state=tk.DISABLED)
            if self.crop_rectangle:
                self.canvas.delete(self.crop_rectangle)
                self.crop_rectangle = None

    def numpy_opreations(self):
        self.arr_image = np.asarray(self.current_image)
    
    def update_display(self):
        if self.current_image:
            # Clear canvas
            self.canvas.delete("all")
            
            # Resize image to fit the window while maintaining aspect ratio
            display_width = self.canvas.winfo_width()
            display_height = self.canvas.winfo_height()
            
            if display_width <= 1 or display_height <= 1:  # Canvas not initialized yet
                display_width = self.image_frame.winfo_width() or 600
                display_height = self.image_frame.winfo_height() or 400
            
            img_width, img_height = self.current_image.size
            
            # Calculate the scaling factor
            width_ratio = display_width / img_width
            height_ratio = display_height / img_height
            self.scale_factor = min(width_ratio, height_ratio)
            
            new_width = int(img_width * self.scale_factor)
            new_height = int(img_height * self.scale_factor)
            
            # Resize the image
            resized_image = self.current_image.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert to PhotoImage
            self.display_image = ImageTk.PhotoImage(resized_image)
            
            # Calculate position to center the image
            x_pos = (display_width - new_width) // 2
            y_pos = (display_height - new_height) // 2
            
            # Add image to canvas
            self.canvas.create_image(x_pos, y_pos, anchor=tk.NW, image=self.display_image)
            
            # Store image position for crop calculations
            self.image_position = (x_pos, y_pos, new_width, new_height)
    
    def apply_blur(self):
        if self.current_image:
            self.current_image = self.current_image.filter(ImageFilter.GaussianBlur(radius=2))
            self.update_display()
            self.status_label.config(text="Applied blur filter")
    
    def apply_sharpen(self):
        if self.current_image:
            enhancer = ImageEnhance.Sharpness(self.current_image)
            self.current_image = enhancer.enhance(2.0)
            self.update_display()
            self.status_label.config(text="Applied sharpen filter")
    
    def apply_grayscale(self):
        if self.current_image:
            self.current_image = self.current_image.convert('L').convert('RGB')
            self.update_display()
            self.status_label.config(text="Applied grayscale filter")
    
    def rot_img(self):
        self.numpy_opreations()
        # self.rotate_arr = self.arr_image
        self.arr_image = np.rot90(self.arr_image)

        self.current_image = Image.fromarray(self.arr_image)
        self.update_display()

        self.status_label.config(text='Image rotated')
    
    def toggle_crop_mode(self):
        if self.current_image:
            self.crop_mode = not self.crop_mode
            
            if self.crop_mode:
                self.crop_button.config(relief=tk.SUNKEN)
                self.status_label.config(text="Crop Mode: Select area to crop")
                # Clear any existing crop rectangle
                if self.crop_rectangle:
                    self.canvas.delete(self.crop_rectangle)
                    self.crop_rectangle = None
                self.apply_crop_button.config(state=tk.DISABLED)
            else:
                self.crop_button.config(relief=tk.RAISED)
                self.status_label.config(text="Crop Mode disabled")
                # Clear any existing crop rectangle
                if self.crop_rectangle:
                    self.canvas.delete(self.crop_rectangle)
                    self.crop_rectangle = None
                self.apply_crop_button.config(state=tk.DISABLED)
    
    def on_mouse_down(self, event):
        if self.crop_mode and self.current_image:
            # Store the starting position
            self.crop_start_x = event.x
            self.crop_start_y = event.y
            
            # Clear any existing rectangle
            if self.crop_rectangle:
                self.canvas.delete(self.crop_rectangle)
                self.crop_rectangle = None
    
    def on_mouse_drag(self, event):
        if self.crop_mode and self.current_image and self.crop_start_x is not None:
            # Update end position
            self.crop_end_x = event.x
            self.crop_end_y = event.y
            
            # Redraw the rectangle
            if self.crop_rectangle:
                self.canvas.delete(self.crop_rectangle)
            
            self.crop_rectangle = self.canvas.create_rectangle(
                self.crop_start_x, self.crop_start_y, 
                self.crop_end_x, self.crop_end_y,
                outline="red", width=2
            )
    
    def on_mouse_up(self, event):
        if self.crop_mode and self.current_image and self.crop_start_x is not None:
            # Finalize end position
            self.crop_end_x = event.x
            self.crop_end_y = event.y
            
            # Check if we have a valid selection
            if (abs(self.crop_end_x - self.crop_start_x) > 10 and 
                abs(self.crop_end_y - self.crop_start_y) > 10):
                self.apply_crop_button.config(state=tk.NORMAL)
                self.status_label.config(text="Crop area selected. Click 'Apply Crop' to crop.")
            else:
                if self.crop_rectangle:
                    self.canvas.delete(self.crop_rectangle)
                    self.crop_rectangle = None
                self.apply_crop_button.config(state=tk.DISABLED)
                self.status_label.config(text="Selection too small. Try again.")
    
    def apply_crop(self):
        if (self.current_image and self.crop_rectangle and 
            self.crop_start_x is not None and self.crop_end_x is not None):
            
            # Get image position and size from canvas
            img_x, img_y, img_width, img_height = self.image_position
            
            # Convert canvas coordinates to image coordinates
            start_x = max(0, (self.crop_start_x - img_x) / self.scale_factor)
            start_y = max(0, (self.crop_start_y - img_y) / self.scale_factor)
            end_x = min(self.current_image.width, (self.crop_end_x - img_x) / self.scale_factor)
            end_y = min(self.current_image.height, (self.crop_end_y - img_y) / self.scale_factor)
            
            # Ensure start is less than end
            if start_x > end_x:
                start_x, end_x = end_x, start_x
            if start_y > end_y:
                start_y, end_y = end_y, start_y
            
            # Crop the image
            self.current_image = self.current_image.crop((int(start_x), int(start_y), int(end_x), int(end_y)))
            
            # Clear crop rectangle
            if self.crop_rectangle:
                self.canvas.delete(self.crop_rectangle)
                self.crop_rectangle = None
            
            # Exit crop mode
            self.crop_mode = False
            self.crop_button.config(relief=tk.RAISED)
            self.apply_crop_button.config(state=tk.DISABLED)
            
            # Update display
            self.update_display()
            self.status_label.config(text="Image cropped successfully")
    
    def save_image(self):
        if self.current_image:
            # Get original filename and directory
            original_dir = os.path.dirname(self.file_path) if self.file_path else ""
            original_filename = os.path.basename(self.file_path) if self.file_path else "filtered_image.png"
            filename, extension = os.path.splitext(original_filename)
            
            # Suggest a new filename
            suggested_filename = f"{filename}_edited{extension}"
            
            # Open save dialog
            save_path = filedialog.asksaveasfilename(
                initialdir=original_dir,
                initialfile=suggested_filename,
                defaultextension=extension,
                filetypes=[
                    ("JPEG files", "*.jpg *.jpeg"),
                    ("PNG files", "*.png"),
                    ("BMP files", "*.bmp"),
                    ("All files", "*.*")
                ]
            )
            
            if save_path:
                try:
                    # Save the image
                    self.current_image.save(save_path)
                    self.status_label.config(text=f"Image saved successfully: {save_path}")
                except Exception as e:
                    self.status_label.config(text=f"Error saving image: {str(e)}")

# Handle window resize
def on_resize(event):
    if hasattr(app, 'current_image') and app.current_image:
        app.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageFilterApp(root)
    
    # Bind resize event
    root.bind("<Configure>", on_resize)
    
    root.mainloop()