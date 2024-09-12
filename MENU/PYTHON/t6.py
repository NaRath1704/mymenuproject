from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation
import pyautogui

# Hardcoded key mappings
key_mappings = {
    'mute': 'ctrl+f1',
    'decrease_volume': 'ctrl+f2',
    'increase_volume': 'ctrl+f3'
}

# Function to simulate key press
def press_key(key_combination):
    try:
        if key_combination:
            pyautogui.hotkey(*key_combination.split('+'))
    except Exception as e:
        print(f"Error simulating key press: {e}")

# Functions to control volume
def mute_volume(instance):
    press_key(key_mappings['mute'])

def decrease_volume(instance):
    press_key(key_mappings['decrease_volume'])

def increase_volume(instance):
    press_key(key_mappings['increase_volume'])

# Custom button class with rounded corners and shadow effect
class CustomButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (200, 50)
        self.pos_hint = {'center_x': 0.5}

        # Add canvas instructions for button appearance
        with self.canvas.before:
            # Uniform shadow for 3D effect
            self.shadow_color = Color(0, 0, 0, 0.3)
            self.shadow_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
            
            # Button background
            self.bg_color = Color(0.2, 0.2, 0.2, 1)
            self.bg_rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])

        self.bind(size=self._update_rect, pos=self._update_rect)

        # Bind button hover effects
        self.bind(on_enter=self._on_hover, on_leave=self._on_leave)

    def _update_rect(self, instance, value):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.shadow_rect.pos = self.pos
        self.shadow_rect.size = self.size

    def _on_hover(self, instance, *args):
        # Animate button color on hover
        anim = Animation(background_color=(0.3, 0.3, 0.3, 1), duration=0.2)
        anim.start(self)

    def _on_leave(self, instance, *args):
        # Animate button color off hover
        anim = Animation(background_color=(0.2, 0.2, 0.2, 1), duration=0.2)
        anim.start(self)

class VolumeControlApp(App):
    def build(self):
        # Set up window size and icon
        Window.size = (400, 300)
        Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark background

        layout = FloatLayout()

        # Add mute button
        self.mute_button = CustomButton(text='Mute')
        self.mute_button.pos_hint = {'center_x': 0.5, 'y': 0.6}
        self.mute_button.bind(on_press=mute_volume)
        layout.add_widget(self.mute_button)

        # Add increase volume button
        self.increase_button = CustomButton(text='Increase Volume')
        self.increase_button.pos_hint = {'center_x': 0.5, 'y': 0.4}
        self.increase_button.bind(on_press=increase_volume)
        layout.add_widget(self.increase_button)

        # Add decrease volume button
        self.decrease_button = CustomButton(text='Decrease Volume')
        self.decrease_button.pos_hint = {'center_x': 0.5, 'y': 0.2}
        self.decrease_button.bind(on_press=decrease_volume)
        layout.add_widget(self.decrease_button)

        return layout

if __name__ == '__main__':
    VolumeControlApp().run()
