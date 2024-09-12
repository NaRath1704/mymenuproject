#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, messagebox
import json
import boto3
import os

# Read AWS credentials from JSON file
def read_aws_keys(filename):
    with open(filename, 'r') as file:
        keys = json.load(file)
    return keys

# Initialize AWS client
def get_s3_client():
    keys = read_aws_keys(r'MENU\AWS\aws_credentials.json')
    s3 = boto3.client(
        's3',
        aws_access_key_id=keys.get('aws_access_key_id'),
        aws_secret_access_key=keys.get('aws_secret_access_key'),
        region_name='ap-south-1'
    )
    return s3

def create_bucket(bucket_name):
    s3 = get_s3_client()
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            ACL='private',
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-south-1'
            }
        )
        return "Bucket created successfully!"
    except Exception as e:
        return f"Error creating bucket: {str(e)}"

def list_buckets():
    s3 = get_s3_client()
    try:
        buckets = s3.list_buckets()
        return [bucket['Name'] for bucket in buckets['Buckets']]
    except Exception as e:
        return []

def list_files(bucket_name):
    s3 = get_s3_client()
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        files = [content['Key'] for content in response.get('Contents', [])]
        return files
    except Exception as e:
        return []

def generate_presigned_url(bucket_name, object_name):
    s3 = get_s3_client()
    try:
        url = s3.generate_presigned_url('get_object',
                                        Params={'Bucket': bucket_name, 'Key': object_name},
                                        ExpiresIn=3600)
        return url
    except Exception as e:
        return None

def upload_file(bucket_name, file_path):
    s3 = get_s3_client()
    try:
        s3.upload_file(file_path, bucket_name, os.path.basename(file_path))
        return "File uploaded successfully!"
    except Exception as e:
        return f"Error uploading file: {str(e)}"

class S3ManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("S3 Bucket Manager")

        # Set window icon (convert to .ico if not already)
        try:
            self.root.iconbitmap(r'MENU\assets\Simple Storage Service.ico')
        except Exception as e:
            print(f"Error loading icon: {e}")

        # Center the window on the screen
        self.center_window(800, 600)

        # Create widgets
        self.create_widgets()

    def center_window(self, width, height):
        # Get the dimensions of the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate position x, y
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        
        # Set the dimensions of the window and where it is placed
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def create_widgets(self):
        # Bucket Creation
        tk.Label(self.root, text="Create S3 Bucket").pack(pady=10)
        self.bucket_name_entry = tk.Entry(self.root, width=50)
        self.bucket_name_entry.pack(pady=5)
        tk.Button(self.root, text="Create Bucket", command=self.create_bucket).pack(pady=5)

        # File Upload
        tk.Label(self.root, text="Upload File to S3 Bucket").pack(pady=10)
        self.upload_bucket_name_var = tk.StringVar(self.root)
        self.upload_bucket_name_var.set("Select a bucket")  # Default value
        self.upload_bucket_menu = tk.OptionMenu(self.root, self.upload_bucket_name_var, *self.get_buckets())
        self.upload_bucket_menu.pack(pady=5)
        tk.Button(self.root, text="Choose File", command=self.choose_file).pack(pady=5)
        self.file_path = None
        tk.Button(self.root, text="Upload File", command=self.upload_file).pack(pady=5)

        # List Files
        tk.Label(self.root, text="List Files in S3 Bucket").pack(pady=10)
        self.list_bucket_name_var = tk.StringVar(self.root)
        self.list_bucket_name_var.set("Select a bucket")  # Default value
        self.list_bucket_menu = tk.OptionMenu(self.root, self.list_bucket_name_var, *self.get_buckets())
        self.list_bucket_menu.pack(pady=5)
        tk.Button(self.root, text="List Files", command=self.list_files).pack(pady=5)

        self.result_text = tk.Text(self.root, height=10, width=160)  # Width adjusted to be wider
        self.result_text.pack(pady=10)

    def get_buckets(self):
        return list_buckets()

    def update_bucket_options(self):
        buckets = self.get_buckets()
        self.upload_bucket_name_var.set("Select a bucket")  # Reset default value
        self.list_bucket_name_var.set("Select a bucket")  # Reset default value

        # Update upload bucket menu
        menu = self.upload_bucket_menu['menu']
        menu.delete(0, 'end')
        for bucket in buckets:
            menu.add_command(label=bucket, command=tk._setit(self.upload_bucket_name_var, bucket))

        # Update list bucket menu
        menu = self.list_bucket_menu['menu']
        menu.delete(0, 'end')
        for bucket in buckets:
            menu.add_command(label=bucket, command=tk._setit(self.list_bucket_name_var, bucket))

    def create_bucket(self):
        bucket_name = self.bucket_name_entry.get()
        if bucket_name:
            result = create_bucket(bucket_name)
            messagebox.showinfo("Result", result)
            self.update_bucket_options()  # Update the bucket lists after creating a new bucket
        else:
            messagebox.showwarning("Input Error", "Bucket name is required!")

    def choose_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            messagebox.showinfo("File Selected", f"Selected file: {os.path.basename(self.file_path)}")

    def upload_file(self):
        bucket_name = self.upload_bucket_name_var.get()
        if bucket_name and self.file_path:
            result = upload_file(bucket_name, self.file_path)
            messagebox.showinfo("Result", result)
        else:
            messagebox.showwarning("Input Error", "Bucket name and file are required!")

    def list_files(self):
        bucket_name = self.list_bucket_name_var.get()
        if bucket_name:
            files = list_files(bucket_name)
            self.result_text.delete(1.0, tk.END)
            if files:
                for file in files:
                    url = generate_presigned_url(bucket_name, file)
                    self.result_text.insert(tk.END, f"{file} - {url}\n")
            else:
                self.result_text.insert(tk.END, "No files found or error retrieving files.")
        else:
            messagebox.showwarning("Input Error", "Bucket name is required!")

if __name__ == "__main__":
    root = tk.Tk()
    app = S3ManagerApp(root)
    root.mainloop()
