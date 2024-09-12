import tkinter as tk
from tkinter import messagebox, scrolledtext
import boto3
import json

# Function to read AWS credentials from a JSON file
def read_aws_keys(filename):
    with open(filename, 'r') as file:
        keys = json.load(file)
    return keys

# Function to get logs from CloudWatch Logs
def get_logs(log_group_name, log_stream_name, region_name, aws_access_key_id, aws_secret_access_key):
    try:
        # Create a CloudWatch Logs client with explicit credentials
        client = boto3.client(
            'logs',
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        # Get log events
        response = client.get_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            startFromHead=True  # Set to False to get the latest logs first
        )

        # Format log events
        logs = []
        for event in response['events']:
            logs.append(str(event['timestamp']) + ' ' + event['message'])

        return '\n'.join(logs)

    except Exception as e:
        return f"Error retrieving logs: {str(e)}"

# Function to handle the button click
def fetch_logs():
    log_group_name = log_group_name_entry.get()
    log_stream_name = log_stream_name_entry.get()
    region_name = region_entry.get()

    # Load AWS credentials
    aws_credentials = read_aws_keys(r'MENU\AWS\aws_credentials.json')
    aws_access_key_id = aws_credentials.get('aws_access_key_id')
    aws_secret_access_key = aws_credentials.get('aws_secret_access_key')

    if log_group_name and log_stream_name and region_name:
        logs = get_logs(log_group_name, log_stream_name, region_name, aws_access_key_id, aws_secret_access_key)
        logs_text_area.delete(1.0, tk.END)
        logs_text_area.insert(tk.END, logs)
    else:
        messagebox.showwarning("Input Error", "All fields are required!")

# Main Tkinter window
root = tk.Tk()
root.title("AWS CloudWatch Logs Viewer")

# Set window icon
root.iconbitmap(r'MENU\assets\CloudWatch.ico')

# Increase width of result box
result_box_width = 100

# Create widgets
tk.Label(root, text="Log Group Name:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
log_group_name_entry = tk.Entry(root, width=50)
log_group_name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Log Stream Name:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
log_stream_name_entry = tk.Entry(root, width=50)
log_stream_name_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="AWS Region:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
region_entry = tk.Entry(root, width=50)
region_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Button(root, text="Fetch Logs", command=fetch_logs).grid(row=3, column=0, columnspan=2, pady=10)

# Create the result box
logs_text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=result_box_width, height=20)
logs_text_area.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Function to center the window
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
