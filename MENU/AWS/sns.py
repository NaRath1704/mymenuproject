import tkinter as tk
from tkinter import messagebox
import boto3
import json

# Function to read AWS credentials from JSON file
def read_aws_keys(filename):
    with open(filename, 'r') as file:
        keys = json.load(file)
    return keys

class SNSTopicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Create SNS Topic")

        # Center the window
        self.center_window(300, 150)

        # Set the window icon (optional, make sure it's a valid .ico file)
        self.root.iconbitmap(r'MENU\assets\Simple Notification Service.ico')

        # AWS Credentials
        self.aws_credentials = read_aws_keys(r'MENU\AWS\aws_credentials.json')

        # GUI Elements
        tk.Label(self.root, text="Enter Topic Name:").pack(pady=10)
        self.topic_name_entry = tk.Entry(self.root, width=30)
        self.topic_name_entry.pack(pady=5)

        tk.Button(self.root, text="Create Topic", command=self.create_topic).pack(pady=10)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_topic(self):
        topic_name = self.topic_name_entry.get()
        if not topic_name:
            messagebox.showwarning("Input Error", "Please enter a topic name.")
            return

        # Create SNS client using credentials from the JSON file
        session = boto3.Session(
            aws_access_key_id=self.aws_credentials['aws_access_key_id'],
            aws_secret_access_key=self.aws_credentials['aws_secret_access_key'],
            region_name=self.aws_credentials.get('region_name', 'ap-south-1')
        )

        sns_client = session.client('sns')

        try:
            response = sns_client.create_topic(Name=topic_name)
            topic_arn = response['TopicArn']
            messagebox.showinfo("Success", f"Topic created successfully!\nTopic ARN: {topic_arn}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create topic: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SNSTopicApp(root)
    root.mainloop()
