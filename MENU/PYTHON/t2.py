import uiautomator2 as u2
import tkinter as tk
import subprocess
import pyautogui
import time
import psutil
from tkinter import messagebox, PhotoImage

def center_window(window, width=400, height=200):
    # Increase height by 1.25 times
    new_height = int(height * 1.25)
    
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (new_height // 2)
    window.geometry(f"{width}x{new_height}+{x}+{y}")

def get_sms_details():
    recipient_number = ""
    message_text = ""

    def submit():
        nonlocal recipient_number, message_text
        recipient_number = entry_recipient.get()
        message_text = entry_message.get()
        root.destroy()

    root = tk.Tk()
    root.title("SMS Sender")

    try:
        icon = PhotoImage(file=r"C:\Users\Nannu\Desktop\soft\MENU\assets\t2.png")
        root.iconphoto(True, icon)
    except tk.TclError:
        print("Icon file not found or could not be loaded.")

    center_window(root, width=400, height=200)

    font = ('Arial', 12)
    padding = {'padx': 10, 'pady': 5}

    tk.Label(root, text="Enter the recipient's phone number:", font=font).pack(**padding)
    entry_recipient = tk.Entry(root, font=font)
    entry_recipient.pack(**padding)

    tk.Label(root, text="Enter the message to send (emojis supported):", font=font).pack(**padding)
    entry_message = tk.Entry(root, font=font)
    entry_message.pack(**padding)

    submit_button = tk.Button(root, text="Submit", font=font, bg="#4CAF50", fg="white", command=submit)
    submit_button.pack(pady=20)

    def on_enter(event):
        submit_button.config(bg="#45a049")

    def on_leave(event):
        submit_button.config(bg="#4CAF50")

    submit_button.bind("<Enter>", on_enter)
    submit_button.bind("<Leave>", on_leave)

    root.attributes('-topmost', True)  # Ensure window is always on top
    root.mainloop()

    return recipient_number, message_text

def send_sms_using_uiautomator(recipient_number, message_text):
    d = u2.connect()

    d.screen_on()
    d.press("home")
    d(descriptionContains="Messages").click()

    d(className="android.widget.TextView", text="Messages").wait(timeout=10)
    d(description="Start chat").click()

    d(className="android.widget.EditText").set_text(recipient_number)
    d.press("enter")
    
    message_input = d(className="android.widget.EditText", text="Text message")
    if message_input.exists:
        message_input.clear_text()
    
    message_input.set_text(message_text)
    d(className="android.view.View", resourceId="Compose:Draft:Send", clickable=True).click()

    print("SMS sent!")

def launch_vysor():
    try:
        vysor_path = r"C:\Users\Nannu\AppData\Local\vysor\Vysor.exe"  # Ensure this path is correct
        vysor_process = subprocess.Popen([vysor_path])
        print("Vysor launched successfully.")

        # Wait a few seconds to ensure Vysor has fully launched
        time.sleep(5)

        # Move the mouse to the coordinates and left-click
        pyautogui.moveTo(x=885, y=145)
        pyautogui.click()

        print("Left-clicked at the 'View device' button location.")

        while True:
            recipient_number, message_text = get_sms_details()

            if recipient_number and message_text:
                send_sms_using_uiautomator(recipient_number, message_text)
                # Alert for SMS sent
                messagebox.showinfo("Success", "SMS sent successfully!")
                # Ask if the user wants to send another SMS
                if not messagebox.askyesno("Continue?", "Would you like to send another SMS?"):
                    break
            else:
                print("Recipient number or message text not provided.")
                break

    except Exception as e:
        print(f"Failed to launch Vysor or automate the process: {e}")

    finally:
        # Ensure Vysor is closed
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if proc.info['name'] == 'Vysor.exe':
                try:
                    proc.terminate()
                    proc.wait(timeout=5)
                except psutil.NoSuchProcess:
                    pass
                except psutil.AccessDenied:
                    pass

if __name__ == "__main__":
    launch_vysor()
