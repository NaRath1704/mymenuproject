import tkinter as tk
from tkinter import filedialog, colorchooser, Menu
from PIL import Image, ImageTk, ImageGrab
import pyautogui
import os

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Paint App")
        self.root.iconphoto(False, tk.PhotoImage(file='MENU/assets/paint-palette.png'))

        self.brush_color = "black"
        self.brush_size = 2
        self.undo_stack = []
        self.redo_stack = []

        # Set up the canvas
        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Set up the buttons and options
        self.setup_buttons()

        # Bind mouse events to canvas
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonPress-1>", self.start_paint)
        self.canvas.bind("<ButtonRelease-1>", self.stop_paint)

        # Store line coordinates for undo/redo
        self.current_line = None

    def setup_buttons(self):
        button_frame = tk.Frame(self.root, padx=5, pady=5)
        button_frame.pack(side=tk.TOP, fill=tk.X)

        # Brush size button with dropdown
        brush_img = Image.open('MENU/assets/brush.png')
        brush_img = brush_img.resize((30, 30), Image.LANCZOS)
        self.brush_icon = ImageTk.PhotoImage(brush_img)
        brush_button = tk.Menubutton(button_frame, image=self.brush_icon)
        brush_button.menu = Menu(brush_button, tearoff=0)
        brush_button["menu"] = brush_button.menu

        for size in [2, 5, 10, 20, 40]:
            brush_button.menu.add_command(label=str(size), command=lambda s=size: self.change_brush_size(s))

        brush_button.pack(side=tk.LEFT, padx=2)

        # Color chooser button
        color_img = Image.open('MENU/assets/color-wheel.png')
        color_img = color_img.resize((30, 30), Image.LANCZOS)
        self.color_icon = ImageTk.PhotoImage(color_img)
        color_button = tk.Button(button_frame, image=self.color_icon, command=self.choose_color)
        color_button.image = self.color_icon  # Keep a reference to prevent garbage collection
        color_button.pack(side=tk.LEFT, padx=2)

        # Undo and Redo buttons with icons
        undo_image = Image.open('MENU/assets/undo.png')
        undo_image = undo_image.resize((30, 30), Image.LANCZOS)
        undo_icon = ImageTk.PhotoImage(undo_image)
        undo_button = tk.Button(button_frame, image=undo_icon, command=self.undo)
        undo_button.image = undo_icon  # Keep a reference to prevent garbage collection
        undo_button.pack(side=tk.LEFT, padx=2)

        redo_image = Image.open('MENU/assets/redo (2).png')
        redo_image = redo_image.resize((30, 30), Image.LANCZOS)
        redo_icon = ImageTk.PhotoImage(redo_image)
        redo_button = tk.Button(button_frame, image=redo_icon, command=self.redo)
        redo_button.image = redo_icon  # Keep a reference to prevent garbage collection
        redo_button.pack(side=tk.LEFT, padx=2)

        # Eraser button with icon
        eraser_img = Image.open('MENU/assets/eraser.png')
        eraser_img = eraser_img.resize((30, 30), Image.LANCZOS)
        eraser_icon = ImageTk.PhotoImage(eraser_img)
        eraser_button = tk.Button(button_frame, image=eraser_icon, command=self.use_eraser)
        eraser_button.image = eraser_icon  # Keep a reference to prevent garbage collection
        eraser_button.pack(side=tk.LEFT, padx=2)

        # Import image button with icon
        import_img = Image.open('MENU/assets/photo-editing_11733558.png')
        import_img = import_img.resize((30, 30), Image.LANCZOS)
        import_icon = ImageTk.PhotoImage(import_img)
        import_button = tk.Button(button_frame, image=import_icon, command=self.import_image)
        import_button.image = import_icon  # Keep a reference to prevent garbage collection
        import_button.pack(side=tk.LEFT, padx=2)

        # Clear canvas button with icon
        clear_img = Image.open('MENU/assets/reset.png')
        clear_img = clear_img.resize((30, 30), Image.LANCZOS)
        clear_icon = ImageTk.PhotoImage(clear_img)
        clear_button = tk.Button(button_frame, image=clear_icon, command=self.clear_canvas)
        clear_button.image = clear_icon  # Keep a reference to prevent garbage collection
        clear_button.pack(side=tk.LEFT, padx=2)

        # Save image button with icon
        save_img = Image.open('MENU/assets/saveimage.png')
        save_img = save_img.resize((30, 30), Image.LANCZOS)
        save_icon = ImageTk.PhotoImage(save_img)
        save_button = tk.Button(button_frame, image=save_icon, command=self.save_image)
        save_button.image = save_icon  # Keep a reference to prevent garbage collection
        save_button.pack(side=tk.LEFT, padx=2)

    def change_brush_size(self, size):
        self.brush_size = size

    def choose_color(self):
        self.brush_color = colorchooser.askcolor(color=self.brush_color)[1]

    def use_eraser(self):
        self.brush_color = "white"

    def start_paint(self, event):
        self.current_line = [(event.x, event.y)]

    def paint(self, event):
        x, y = event.x, event.y
        self.canvas.create_line(self.current_line[-1], (x, y), fill=self.brush_color, width=self.brush_size, capstyle=tk.ROUND, smooth=tk.TRUE)
        self.current_line.append((x, y))

    def stop_paint(self, event):
        if self.current_line:
            self.undo_stack.append(self.current_line)
            self.redo_stack.clear()
            self.current_line = None

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.undo_stack.pop())
            self.redraw_canvas()

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.redo_stack.pop())
            self.redraw_canvas()

    def redraw_canvas(self):
        self.canvas.delete("all")
        for line in self.undo_stack:
            for i in range(1, len(line)):
                self.canvas.create_line(line[i-1], line[i], fill=self.brush_color, width=self.brush_size, capstyle=tk.ROUND, smooth=tk.TRUE)

    def import_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            img = Image.open(file_path)
            img.thumbnail((800, 600))  # Resize to fit canvas
            self.imported_image = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imported_image)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.undo_stack.clear()
        self.redo_stack.clear()

    def save_image(self):
        # Get the canvas's bounding box and take a screenshot
        x1 = self.root.winfo_rootx() + self.canvas.winfo_x()
        y1 = self.root.winfo_rooty() + self.canvas.winfo_y()
        x2 = x1 + self.canvas.winfo_width()
        y2 = y1 + self.canvas.winfo_height()

        # Capture the screenshot
        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        
        # Ask for the save location
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                               filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            screenshot.save(file_path)
            print(f"Image saved successfully as {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
