import os
import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, simpledialog
from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageDraw, ImageFont

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Image Editor")
        self.root.geometry("1200x700")
        
        # Variables
        self.image_path = None
        self.original_image = None
        self.current_image = None
        self.display_image = None
        self.image_tk = None
        self.text_to_add = []
        self.is_drawing = False
        self.last_x, self.last_y = 0, 0
        self.brush_color = "#000000"
        self.brush_size = 2
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for buttons
        self.left_panel = ttk.Frame(self.main_frame, width=200)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Canvas for image display
        self.canvas_frame = ttk.Frame(self.main_frame)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="#f0f0f0", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        self.h_scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.v_scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)
        
        # Create UI elements
        self.create_ui()
        
        # Canvas events for drawing
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Welcome to Image Editor", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_ui(self):
        # Section label
        ttk.Label(self.left_panel, text="File Operations", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # File operations
        ttk.Button(self.left_panel, text="Browse Image", command=self.browse_image).grid(row=1, column=0, sticky="ew", pady=2)
        ttk.Button(self.left_panel, text="Save Image", command=self.save_image).grid(row=2, column=0, sticky="ew", pady=2)
        ttk.Button(self.left_panel, text="Reset Image", command=self.reset_image).grid(row=3, column=0, sticky="ew", pady=2)
        
        # Separator
        ttk.Separator(self.left_panel, orient=tk.HORIZONTAL).grid(row=4, column=0, sticky="ew", pady=10)
        
        # Basic edits label
        ttk.Label(self.left_panel, text="Basic Edits", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky="w", pady=(0, 5))
        
        # Basic edit operations
        ttk.Button(self.left_panel, text="Rotate Left", command=lambda: self.rotate_image(-90)).grid(row=6, column=0, sticky="ew", pady=2)
        ttk.Button(self.left_panel, text="Rotate Right", command=lambda: self.rotate_image(90)).grid(row=7, column=0, sticky="ew", pady=2)
        ttk.Button(self.left_panel, text="Flip Horizontal", command=lambda: self.flip_image("horizontal")).grid(row=8, column=0, sticky="ew", pady=2)
        ttk.Button(self.left_panel, text="Flip Vertical", command=lambda: self.flip_image("vertical")).grid(row=9, column=0, sticky="ew", pady=2)
        
        # Separator
        ttk.Separator(self.left_panel, orient=tk.HORIZONTAL).grid(row=10, column=0, sticky="ew", pady=10)
        
        # Adjustments label
        ttk.Label(self.left_panel, text="Adjustments", font=("Arial", 10, "bold")).grid(row=11, column=0, sticky="w", pady=(0, 5))
        
        # Adjustments operations
        ttk.Button(self.left_panel, text="Brightness", command=lambda: self.adjust_image("brightness")).grid(row=12, column=0, sticky="ew", pady=2)
        ttk.Button(self.left_panel, text="Contrast", command=lambda: self.adjust_image("contrast")).grid(row=13, column=0, sticky="ew", pady=2)
        ttk.Button(self.left_panel, text="Saturation", command=lambda: self.adjust_image("saturation")).grid(row=14, column=0, sticky="ew", pady=2)
        ttk.Button(self.left_panel, text="Sharpness", command=lambda: self.adjust_image("sharpness")).grid(row=15, column=0, sticky="ew", pady=2)
        
        # Separator
        ttk.Separator(self.left_panel, orient=tk.HORIZONTAL).grid(row=16, column=0, sticky="ew", pady=10)
        
        # Filters label
        ttk.Label(self.left_panel, text="Filters", font=("Arial", 10, "bold")).grid(row=17, column=0, sticky="w", pady=(0, 5))
        
        # Filters operations
        ttk.Button(self.left_panel, text="Blur", command=lambda: self.apply_filter("blur")).grid(row=25, column=0, sticky="ew", pady=2)
        ttk.Button(self.left_panel, text="Sharpen", command=lambda: self.apply_filter("sharpen")).grid(row=26, column=0, sticky="ew", pady=2)
        ttk.Button(self.left_panel, text="Emboss", command=lambda: self.apply_filter("emboss")).grid(row=27, column=0, sticky="ew", pady=2)
        ttk.Button(self.left_panel, text="Edge Enhance", command=lambda: self.apply_filter("edge_enhance")).grid(row=21, column=0, sticky="ew", pady=2)
        ttk.Button(self.left_panel, text="Grayscale", command=lambda: self.apply_filter("grayscale")).grid(row=22, column=0, sticky="ew", pady=2)
        
        # Separator
        ttk.Separator(self.left_panel, orient=tk.HORIZONTAL).grid(row=23, column=0, sticky="ew", pady=10)
        
        # Text and drawing label
        ttk.Label(self.left_panel, text="Text & Drawing", font=("Arial", 10, "bold")).grid(row=24, column=0, sticky="w", pady=(0, 5))
        
        # Text and drawing operations
        ttk.Button(self.left_panel, text="Add Text", command=self.add_text).grid(row=18, column=0, sticky="ew", pady=2)
        ttk.Button(self.left_panel, text="Draw Mode", command=self.toggle_draw_mode).grid(row=19, column=0, sticky="ew", pady=2)
        ttk.Button(self.left_panel, text="Pick Color", command=self.pick_color).grid(row=20, column=0, sticky="ew", pady=2)
        
        # Brush size frame
        brush_frame = ttk.Frame(self.left_panel)
        brush_frame.grid(row=28, column=0, sticky="ew", pady=2)
        
        ttk.Label(brush_frame, text="Brush Size:").pack(side=tk.LEFT)
        self.brush_size_var = tk.IntVar(value=2)
        ttk.Spinbox(brush_frame, from_=1, to=20, width=5, textvariable=self.brush_size_var, command=self.update_brush_size).pack(side=tk.RIGHT)
        
        # Configure the grid
        self.left_panel.grid_columnconfigure(0, weight=1)
    
    def browse_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        
        if file_path:
            self.image_path = file_path
            try:
                self.original_image = Image.open(file_path)
                self.current_image = self.original_image.copy()
                self.display_image_on_canvas()
                self.status_bar.config(text=f"Loaded image: {os.path.basename(file_path)}")
            except Exception as e:
                self.status_bar.config(text=f"Error loading image: {str(e)}")
    
    def display_image_on_canvas(self):
        if self.current_image:
            self.canvas.delete("all")
            self.image_tk = ImageTk.PhotoImage(self.current_image)
            
            # Reset the scroll region
            self.canvas.config(scrollregion=(0, 0, self.current_image.width, self.current_image.height))
            
            # Add image to canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
            
            # Add text overlays if any
            for text_item in self.text_to_add:
                text, x, y, font_size, color = text_item
                self.canvas.create_text(x, y, text=text, fill=color, font=("Arial", font_size), anchor=tk.NW)
    
    def save_image(self):
        if self.current_image:
            # Apply any text overlays to the image
            if self.text_to_add:
                img_draw = ImageDraw.Draw(self.current_image)
                for text_item in self.text_to_add:
                    text, x, y, font_size, color = text_item
                    try:
                        font = ImageFont.truetype("arial.ttf", font_size)
                    except:
                        font = ImageFont.load_default()
                    img_draw.text((x, y), text, fill=color, font=font)
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            
            if file_path:
                try:
                    self.current_image.save(file_path)
                    self.status_bar.config(text=f"Image saved to: {os.path.basename(file_path)}")
                except Exception as e:
                    self.status_bar.config(text=f"Error saving image: {str(e)}")
    
    def reset_image(self):
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.text_to_add = []
            self.display_image_on_canvas()
            self.status_bar.config(text="Image reset to original")
    
    def rotate_image(self, degrees):
        if self.current_image:
            self.current_image = self.current_image.rotate(degrees, expand=True)
            self.display_image_on_canvas()
            self.status_bar.config(text=f"Image rotated by {degrees} degrees")
    
    def flip_image(self, direction):
        if self.current_image:
            if direction == "horizontal":
                self.current_image = self.current_image.transpose(Image.FLIP_LEFT_RIGHT)
                self.status_bar.config(text="Image flipped horizontally")
            elif direction == "vertical":
                self.current_image = self.current_image.transpose(Image.FLIP_TOP_BOTTOM)
                self.status_bar.config(text="Image flipped vertically")
            self.display_image_on_canvas()
    
    def adjust_image(self, adjustment_type):
        if not self.current_image:
            return
        
        value = simpledialog.askfloat(
            f"Adjust {adjustment_type.capitalize()}", 
            f"Enter {adjustment_type} factor (0.0 to 2.0):",
            minvalue=0.0, maxvalue=2.0, initialvalue=1.0
        )
        
        if value is not None:
            try:
                if adjustment_type == "brightness":
                    enhancer = ImageEnhance.Brightness(self.current_image)
                elif adjustment_type == "contrast":
                    enhancer = ImageEnhance.Contrast(self.current_image)
                elif adjustment_type == "saturation":
                    enhancer = ImageEnhance.Color(self.current_image)
                elif adjustment_type == "sharpness":
                    enhancer = ImageEnhance.Sharpness(self.current_image)
                
                self.current_image = enhancer.enhance(value)
                self.display_image_on_canvas()
                self.status_bar.config(text=f"Applied {adjustment_type} adjustment with factor {value}")
            except Exception as e:
                self.status_bar.config(text=f"Error adjusting image: {str(e)}")
    
    def apply_filter(self, filter_type):
        if not self.current_image:
            return
        
        try:
            if filter_type == "blur":
                self.current_image = self.current_image.filter(ImageFilter.BLUR)
            elif filter_type == "sharpen":
                self.current_image = self.current_image.filter(ImageFilter.SHARPEN)
            elif filter_type == "emboss":
                self.current_image = self.current_image.filter(ImageFilter.EMBOSS)
            elif filter_type == "edge_enhance":
                self.current_image = self.current_image.filter(ImageFilter.EDGE_ENHANCE)
            elif filter_type == "grayscale":
                self.current_image = self.current_image.convert("L").convert("RGB")
            
            self.display_image_on_canvas()
            self.status_bar.config(text=f"Applied {filter_type} filter")
        except Exception as e:
            self.status_bar.config(text=f"Error applying filter: {str(e)}")
    
    def add_text(self):
        if not self.current_image:
            return
        
        text = simpledialog.askstring("Add Text", "Enter text to add:")
        if text:
            font_size = simpledialog.askinteger("Font Size", "Enter font size:", minvalue=8, maxvalue=72, initialvalue=24)
            if font_size:
                color = colorchooser.askcolor(title="Select Text Color")[1]
                if color:
                    self.status_bar.config(text="Click on the image to place the text")
                    
                    def place_text(event):
                        canvas_x = self.canvas.canvasx(event.x)
                        canvas_y = self.canvas.canvasy(event.y)
                        self.text_to_add.append((text, canvas_x, canvas_y, font_size, color))
                        self.display_image_on_canvas()
                        self.canvas.unbind("<Button-1>")
                        self.canvas.bind("<ButtonPress-1>", self.start_draw)
                        self.status_bar.config(text=f"Text added: '{text}'")
                    
                    self.canvas.unbind("<ButtonPress-1>")
                    self.canvas.bind("<Button-1>", place_text)
    
    def toggle_draw_mode(self):
        if self.is_drawing:
            self.is_drawing = False
            self.status_bar.config(text="Draw mode disabled")
        else:
            self.is_drawing = True
            self.status_bar.config(text="Draw mode enabled")
    
    def start_draw(self, event):
        if self.is_drawing and self.current_image:
            self.last_x = self.canvas.canvasx(event.x)
            self.last_y = self.canvas.canvasy(event.y)
    
    def draw(self, event):
        if self.is_drawing and self.current_image:
            x = self.canvas.canvasx(event.x)
            y = self.canvas.canvasy(event.y)
            
            # Draw line on canvas
            self.canvas.create_line(
                self.last_x, self.last_y, x, y,
                width=self.brush_size,
                fill=self.brush_color,
                capstyle=tk.ROUND,
                smooth=tk.TRUE
            )
            
            # Draw on the image
            draw = ImageDraw.Draw(self.current_image)
            draw.line(
                [(self.last_x, self.last_y), (x, y)],
                fill=self.brush_color,
                width=self.brush_size
            )
            
            self.last_x = x
            self.last_y = y
    
    def pick_color(self):
        color = colorchooser.askcolor(title="Select Brush Color")[1]
        if color:
            self.brush_color = color
            self.status_bar.config(text=f"Brush color set to: {color}")
    
    def update_brush_size(self):
        try:
            self.brush_size = self.brush_size_var.get()
            self.status_bar.config(text=f"Brush size set to: {self.brush_size}")
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()