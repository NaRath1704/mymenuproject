import tkinter as tk
from tkinter import messagebox
from gtts import gTTS
import os
import pygame
import tempfile

# Function to convert text to speech
def text_to_speech():
    text = text_input.get("1.0", "end-1c")  # Get text from the text box
    if not text.strip():
        messagebox.showerror("Error", "Please enter some text!")
        return

    try:
        # Generate a unique temporary file name for the output mp3
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            temp_audio_file_path = temp_audio_file.name
        
        # Convert text to speech and save it as the temporary mp3 file
        tts = gTTS(text=text, lang='en')
        tts.save(temp_audio_file_path)
        messagebox.showinfo("Success", f"Text converted to speech and saved as '{temp_audio_file_path}'!")

        # Play the audio if the user chooses to do so
        if play_audio.get():
            play_audio_file(temp_audio_file_path)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert text to speech: {e}")

# Function to play the generated audio file
def play_audio_file(file_path):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to play audio: {e}")

# Function to center the window on the screen
def center_window(window):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

# Initialize the tkinter window
root = tk.Tk()
root.title("Text to Speech Converter")
root.geometry("400x300")
root.resizable(False, False)  # Prevent window resizing

# Set the window icon
icon_path = r"MENU\assets\speaking.png"
root.iconphoto(False, tk.PhotoImage(file=icon_path))

# Center the window on the screen
center_window(root)

# Label for instructions
instruction_label = tk.Label(root, text="Enter text to convert to speech:")
instruction_label.pack(pady=10)

# Text box for entering text
text_input = tk.Text(root, height=5, wrap="word")
text_input.pack(pady=10, padx=20)

# Checkbox to choose whether to play the audio immediately after conversion
play_audio = tk.BooleanVar()
play_audio_check = tk.Checkbutton(root, text="Play audio after conversion", variable=play_audio)
play_audio_check.pack(pady=5)

# Button to trigger the text-to-speech conversion
convert_button = tk.Button(root, text="Convert to Speech", command=text_to_speech)
convert_button.pack(pady=20)

# Run the tkinter main loop
root.mainloop()
