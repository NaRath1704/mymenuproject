import tkinter as tk
from tkinter import messagebox
import requests
from geopy.geocoders import Nominatim

# Function to fetch IP-based location
def get_ip_location():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        
        location_str = data['loc']
        latitude, longitude = map(float, location_str.split(','))
        
        return latitude, longitude
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching IP-based location: {e}")
        return None, None

# Function to fetch location name
def get_location_name(latitude, longitude):
    try:
        # Setting a proper User-Agent to avoid being blocked
        geolocator = Nominatim(user_agent="GeoLocationApp/1.0")
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        address = location.address
        return address
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching location name: {e}")
        return None

# Function triggered on button click
def show_location():
    latitude, longitude = get_ip_location()
    
    if latitude and longitude:
        location_label.config(text=f"Coordinates: Latitude = {latitude}, Longitude = {longitude}")
        
        location_name = get_location_name(latitude, longitude)
        if location_name:
            address_label.config(text=f"Location: {location_name}")
            adjust_window_size(location_name)
        else:
            address_label.config(text="Unable to fetch the location name.")
            adjust_window_size("Unable to fetch the location name.")
    else:
        location_label.config(text="Unable to fetch the coordinates.")
        adjust_window_size("Unable to fetch the coordinates.")

# Adjust the window size based on the text length
def adjust_window_size(location_text):
    root.update_idletasks()
    text_width = address_label.winfo_reqwidth()
    new_width = text_width + 50  # Add some padding
    root.geometry(f"{new_width}x{root.winfo_height()}")

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
root.title("Geo-Coordinates Finder")

# Set the window icon
icon_path = r"MENU\assets\location-on-map.png"
root.iconphoto(False, tk.PhotoImage(file=icon_path))

# Initial window size and layout
root.geometry("400x200")

# Center the window on the screen initially
center_window(root)

# Button to trigger location fetching
fetch_button = tk.Button(root, text="Fetch Location", command=show_location)
fetch_button.pack(pady=20)

# Label to display coordinates
location_label = tk.Label(root, text="")
location_label.pack(pady=10)

# Label to display location name
address_label = tk.Label(root, text="")
address_label.pack(pady=10)

# Center the window after the window size changes
root.update()
center_window(root)

# Run the application
root.mainloop()
