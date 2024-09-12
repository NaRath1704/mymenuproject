import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.graphics.texture import Texture
import cv2
import numpy as np
from tkinter import Tk, filedialog
from kivy.core.window import Window

# Set the window icon
Window.set_icon('MENU/assets/face-detection.png')

# To prevent Tkinter window from showing up
Tk().withdraw()

class ImageFilterApp(App):
    def build(self):
        self.image = None
        self.original_image = None

        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Image display widget
        self.image_widget = Image()
        main_layout.add_widget(self.image_widget)

        # Button layout
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=10)

        # Load Image Button
        load_button = Button(text="Load Image", on_press=self.load_image)
        button_layout.add_widget(load_button)

        # Color Effects Dropdown
        color_effects_dropdown = DropDown()

        effects = [
            ("Grayscale", self.apply_grayscale),
            ("Blur", self.apply_blur),
            ("Edge Detection", self.apply_edge_detection),
            ("Sepia", self.apply_sepia),
            ("Invert", self.apply_invert),
            ("Brightness", self.apply_brightness),
            ("Sharpen", self.apply_sharpen),
            ("Emboss", self.apply_emboss),
            ("Cartoon", self.apply_cartoon)
        ]

        for effect_name, effect_function in effects:
            btn = Button(text=effect_name, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn, ef=effect_function: [color_effects_dropdown.select(btn.text), ef(None)])
            color_effects_dropdown.add_widget(btn)

        color_effects_button = Button(text="Color Effects")
        color_effects_button.bind(on_release=color_effects_dropdown.open)
        button_layout.add_widget(color_effects_button)

        # Sunglasses Filter Button
        sunglasses_button = Button(text="Sunglasses", on_press=self.apply_sunglasses)
        button_layout.add_widget(sunglasses_button)

        # Star Effect Button
        star_button = Button(text="Star Effect", on_press=self.apply_star_effect)
        button_layout.add_widget(star_button)

        # Reset to Original Button
        reset_button = Button(text="Original", on_press=self.reset_image)
        button_layout.add_widget(reset_button)

        main_layout.add_widget(button_layout)
        return main_layout

    def load_image(self, instance):
        # Use Tkinter file dialog to select an image file
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.image = cv2.imread(file_path)
            self.original_image = self.image.copy()
            self.update_image_display(self.image)

    def update_image_display(self, img):
        # Convert the image to a texture and display it in Kivy
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        buf = img_rgb.tobytes()
        texture = Texture.create(size=(img_rgb.shape[1], img_rgb.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        texture.flip_vertical()
        self.image_widget.texture = texture

    def apply_sunglasses(self, instance):
        if self.image is not None:
            sunglasses_img = cv2.imread(r'MENU\assets\sunglass.png', -1)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                # Resize the sunglasses to match the width of the detected face
                sunglasses_img_resized = cv2.resize(sunglasses_img, (w, int(w * sunglasses_img.shape[0] / sunglasses_img.shape[1])))

                # Position the sunglasses slightly higher to align with the eyes
                x1 = x
                y1 = int(y + h / 5)  # Move up the position by reducing the divisor (previously it was h / 4)
                x2 = x1 + sunglasses_img_resized.shape[1]
                y2 = y1 + sunglasses_img_resized.shape[0]

                # Ensure the coordinates are within the image bounds
                if y1 < 0:
                    y1 = 0
                if x1 < 0:
                    x1 = 0
                if x2 > self.image.shape[1]:
                    x2 = self.image.shape[1]
                if y2 > self.image.shape[0]:
                    y2 = self.image.shape[0]

                # Blend the sunglasses image with the face
                alpha_s = sunglasses_img_resized[:, :, 3] / 255.0
                alpha_i = 1.0 - alpha_s

                for c in range(0, 3):
                    self.image[y1:y2, x1:x2, c] = (alpha_s * sunglasses_img_resized[:, :, c] +
                                                   alpha_i * self.image[y1:y2, x1:x2, c])

            self.update_image_display(self.image)

    def apply_star_effect(self, instance):
        if self.image is not None:
            star_img = cv2.imread(r'MENU\assets\stars.png', -1)
            star_img_resized = cv2.resize(star_img, (int(star_img.shape[1] * 0.1), int(star_img.shape[0] * 0.1)))
            img_height, img_width, _ = self.image.shape

            for _ in range(7):  # Place 7 stars randomly
                x_offset = np.random.randint(0, img_width - star_img_resized.shape[1])
                y_offset = np.random.randint(0, img_height - star_img_resized.shape[0])

                x1, y1 = x_offset, y_offset
                x2, y2 = x1 + star_img_resized.shape[1], y1 + star_img_resized.shape[0]

                # Blend the star image with the original image
                alpha_s = star_img_resized[:, :, 3] / 255.0
                alpha_i = 1.0 - alpha_s

                for c in range(0, 3):
                    self.image[y1:y2, x1:x2, c] = (alpha_s * star_img_resized[:, :, c] +
                                                   alpha_i * self.image[y1:y2, x1:x2, c])

            self.update_image_display(self.image)

    def apply_grayscale(self, instance):
        if self.image is not None:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
            self.update_image_display(self.image)

    def apply_blur(self, instance):
        if self.image is not None:
            self.image = cv2.GaussianBlur(self.image, (15, 15), 0)
            self.update_image_display(self.image)

    def apply_edge_detection(self, instance):
        if self.image is not None:
            edges = cv2.Canny(self.image, 100, 200)
            self.image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            self.update_image_display(self.image)

    def apply_sepia(self, instance):
        if self.image is not None:
            sepia_filter = np.array([[0.272, 0.534, 0.131],
                                     [0.349, 0.686, 0.168],
                                     [0.393, 0.769, 0.189]])
            self.image = cv2.transform(self.image, sepia_filter)
            self.image = np.clip(self.image, 0, 255).astype(np.uint8)
            self.update_image_display(self.image)

    def apply_invert(self, instance):
        if self.image is not None:
            self.image = cv2.bitwise_not(self.image)
            self.update_image_display(self.image)

    def apply_brightness(self, brightness=30):
        if self.image is not None:
            self.image = cv2.convertScaleAbs(self.image, beta=brightness)
            self.update_image_display(self.image)

    def apply_sharpen(self, instance):
        if self.image is not None:
            kernel = np.array([[0, -1, 0],
                               [-1, 5, -1],
                               [0, -1, 0]])
            self.image = cv2.filter2D(self.image, -1, kernel)
            self.update_image_display(self.image)

    def apply_emboss(self, instance):
        if self.image is not None:
            kernel = np.array([[2, 0, 0],
                               [0, -1, 0],
                               [0, 0, -1]])
            self.image = cv2.filter2D(self.image, -1, kernel)
            self.update_image_display(self.image)

    def apply_cartoon(self, instance):
        if self.image is not None:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray, 5)
            edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
            color = cv2.bilateralFilter(self.image, 9, 300, 300)
            self.image = cv2.bitwise_and(color, color, mask=edges)
            self.update_image_display(self.image)

    def reset_image(self, instance):
        if self.original_image is not None:
            self.image = self.original_image.copy()
            self.update_image_display(self.image)

if __name__ == '__main__':
    ImageFilterApp().run()
