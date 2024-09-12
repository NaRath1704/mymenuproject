import tkinter as tk
from tkinter import messagebox
import boto3
import json

# Function to read AWS credentials from a JSON file
def read_aws_keys(filename):
    try:
        with open(filename, 'r') as file:
            keys = json.load(file)
        return keys
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load AWS credentials: {e}")
        return {}

# Function to create or delete IAM user
def manage_iam_user(action):
    name = user_name_entry.get()
    if not name:
        messagebox.showwarning("Input Error", "User name cannot be empty!")
        return

    # Load AWS credentials
    aws_credentials = read_aws_keys(r'MENU\AWS\aws_credentials.json')
    aws_access_key_id = aws_credentials.get('aws_access_key_id')
    aws_secret_access_key = aws_credentials.get('aws_secret_access_key')

    if not aws_access_key_id or not aws_secret_access_key:
        messagebox.showerror("Error", "AWS credentials are not set.")
        return

    # Initialize a session using the specified credentials
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name='ap-south-1'
    )
    iam_client = session.client('iam')

    try:
        if action == "create":
            iam_client.create_user(UserName=name)
            messagebox.showinfo("Success", f"IAM user '{name}' created successfully!")
        elif action == "delete":
            iam_client.delete_user(UserName=name)
            messagebox.showinfo("Success", f"IAM user '{name}' deleted successfully!")
        else:
            messagebox.showwarning("Input Error", "Invalid action specified. Please use 'create' or 'delete'.")
    except iam_client.exceptions.EntityAlreadyExistsException:
        messagebox.showerror("Error", f"IAM user '{name}' already exists.")
    except iam_client.exceptions.NoSuchEntityException:
        messagebox.showerror("Error", f"IAM user '{name}' does not exist.")
    except Exception as e:
        messagebox.showerror("Error", f"Error managing IAM user: {e}")

# Function to handle button clicks
def create_user():
    manage_iam_user("create")

def delete_user():
    manage_iam_user("delete")

# Main Tkinter window
root = tk.Tk()
root.title("IAM User Manager")

# Set window icon
root.iconbitmap(r'MENU\assets\IAM Identity Center.ico')

# Create widgets
tk.Label(root, text="IAM User Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
user_name_entry = tk.Entry(root, width=50)
user_name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Button(root, text="Create User", command=create_user).grid(row=1, column=0, padx=10, pady=10)
tk.Button(root, text="Delete User", command=delete_user).grid(row=1, column=1, padx=10, pady=10)

# Center the window
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

# Call function to center the window
center_window(root)

# Fit the window size to its content
root.update_idletasks()
root.minsize(root.winfo_width(), root.winfo_height())

# Run the Tkinter event loop
root.mainloop()
