import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def detect_face(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)):
    """Detects faces in an image and returns the first detected face."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize)
    return faces

def get_face_image(image_path):
    """Extracts the face from the image at image_path."""
    image = cv2.imread(image_path)
    faces = detect_face(image)
    if len(faces) == 0:
        raise Exception("No face detected in the image.")
    (x, y, w, h) = faces[0]
    return image[y:y+h, x:x+w]

def replace_face(main_image_path, face_image):
    """Replaces the detected face in the main image with the face_image."""
    main_image = cv2.imread(main_image_path)
    faces = detect_face(main_image)
    
    if len(faces) == 0:
        raise Exception("No face detected in the main image.")
    
    (x, y, w, h) = faces[0]
    
    # Resize the face image to fit the detected face area
    face_resized = cv2.resize(face_image, (w, h))
    
    # Replace the face in the main image
    main_image[y:y+h, x:x+w] = face_resized
    
    return main_image

def resize_image(image, max_size):
    """Resize the image to fit within max_size dimensions."""
    height, width = image.shape[:2]
    if width > height:
        new_width = max_size
        new_height = int((new_width / width) * height)
    else:
        new_height = max_size
        new_width = int((new_height / height) * width)
    return cv2.resize(image, (new_width, new_height))

def convert_cv_to_pil(image):
    """Convert OpenCV image to PIL image."""
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
    return Image.fromarray(image)

def display_image(image, label):
    """Displays an image using PIL in a Tkinter label."""
    image = convert_cv_to_pil(image)
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo  # Keep a reference to avoid garbage collection

class FaceReplaceApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Face Replacement")
        self.geometry("400x200")
        
        # Set window icon
        self.icon_file = 'MENU/assets/face-detection.png'
        self.iconphoto(False, tk.PhotoImage(file=self.icon_file))

        self.source_image_path = None
        self.main_image_path = None

        # Create buttons
        self.select_source_button = tk.Button(self, text="Select Face Image", command=self.select_source_image)
        self.select_source_button.pack(pady=10)
        
        self.select_main_button = tk.Button(self, text="Select Main Image", command=self.select_main_image)
        self.select_main_button.pack(pady=10)
        
        self.replace_button = tk.Button(self, text="Replace Face", command=self.replace_face)
        self.replace_button.pack(pady=10)

    def select_source_image(self):
        self.source_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    
    def select_main_image(self):
        self.main_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    
    def replace_face(self):
        if not self.source_image_path or not self.main_image_path:
            messagebox.showerror("Error", "Please select both images.")
            return
        
        try:
            face_image = get_face_image(self.source_image_path)
            result_image = replace_face(self.main_image_path, face_image)
            
            # Resize images to fit the result window
            max_size = 250
            face_image_resized = resize_image(face_image, max_size)
            result_image_resized = resize_image(result_image, max_size)
            main_image_resized = resize_image(cv2.imread(self.main_image_path), max_size)
            
            self.show_results_window(face_image_resized, main_image_resized, result_image_resized)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_results_window(self, face_image, main_image, result_image):
        results_window = tk.Toplevel(self)
        results_window.title("Results")
        
        # Set icon for the results window
        results_window.iconphoto(False, tk.PhotoImage(file=self.icon_file))
        
        # Create a frame for the results
        frame = tk.Frame(results_window)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create labels for images and their information
        face_label = tk.Label(frame)
        main_label = tk.Label(frame)
        result_label = tk.Label(frame)
        
        # Display images
        display_image(face_image, face_label)
        display_image(main_image, main_label)
        display_image(result_image, result_label)

        # Pack images
        face_label.grid(row=0, column=0, padx=10, pady=(0, 5))
        main_label.grid(row=0, column=1, padx=10, pady=(0, 5))
        result_label.grid(row=0, column=2, padx=10, pady=(0, 5))

        # Add labels with info below each image
        face_info = tk.Label(frame, text="Face Image", anchor="center")
        main_info = tk.Label(frame, text="Main Image", anchor="center")
        result_info = tk.Label(frame, text="Result Image", anchor="center")

        face_info.grid(row=1, column=0, padx=10, pady=5)
        main_info.grid(row=1, column=1, padx=10, pady=5)
        result_info.grid(row=1, column=2, padx=10, pady=5)

if __name__ == "__main__":
    app = FaceReplaceApp()
    app.mainloop()
