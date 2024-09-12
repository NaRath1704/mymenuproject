import tkinter as tk
from tkinter import messagebox, scrolledtext
import boto3
import json

# Function to read AWS credentials from a JSON file
def read_aws_keys(filename):
    with open(filename, 'r') as file:
        keys = json.load(file)
    return keys

# Function to create a DynamoDB table
def create_table(table_name, key_schema, attribute_definitions, provisioned_throughput):
    try:
        response = dynamodb.create_table(
            TableName=table_name,
            KeySchema=json.loads(key_schema),
            AttributeDefinitions=json.loads(attribute_definitions),
            ProvisionedThroughput=json.loads(provisioned_throughput)
        )
        return response
    except Exception as e:
        return {'error': str(e)}

# Function to list DynamoDB tables
def list_tables():
    try:
        response = dynamodb.list_tables()
        return response
    except Exception as e:
        return {'error': str(e)}

# Function to delete a DynamoDB table
def delete_table(table_name):
    try:
        response = dynamodb.delete_table(TableName=table_name)
        return response
    except Exception as e:
        return {'error': str(e)}

# Function to handle button actions
def handle_action():
    action = action_var.get()
    table_name = table_name_entry.get()
    key_schema = key_schema_entry.get()
    attribute_definitions = attribute_definitions_entry.get()
    provisioned_throughput = provisioned_throughput_entry.get()
    
    if action == 'create_table':
        if table_name and key_schema and attribute_definitions and provisioned_throughput:
            response = create_table(table_name, key_schema, attribute_definitions, provisioned_throughput)
        else:
            response = {'error': 'All fields are required for creating a table.'}
    elif action == 'list_tables':
        response = list_tables()
    elif action == 'delete_table':
        if table_name:
            response = delete_table(table_name)
        else:
            response = {'error': 'Table name is required for deletion.'}
    else:
        response = {'error': 'Invalid action specified.'}

    # Display the response in the text area
    if 'error' in response:
        messagebox.showerror("Error", response['error'])
    else:
        output_text_area.delete(1.0, tk.END)
        output_text_area.insert(tk.END, json.dumps(response, indent=2))

# Load AWS credentials
aws_credentials = read_aws_keys(r'MENU\AWS\aws_credentials.json')
aws_access_key_id = aws_credentials.get('aws_access_key_id')
aws_secret_access_key = aws_credentials.get('aws_secret_access_key')
aws_region = aws_credentials.get('region_name')

# Create a DynamoDB client with the loaded credentials
dynamodb = boto3.client(
    'dynamodb',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

# Main Tkinter window
root = tk.Tk()
root.title("AWS DynamoDB Manager")

root.iconbitmap(r'MENU\assets\DynamoDB.ico')

# Set window size
root.geometry("800x600")

# Create widgets
tk.Label(root, text="Action:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
action_var = tk.StringVar()
action_menu = tk.OptionMenu(root, action_var, 'create_table', 'list_tables', 'delete_table')
action_menu.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Table Name:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
table_name_entry = tk.Entry(root, width=60)
table_name_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Key Schema (JSON):").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
key_schema_entry = tk.Entry(root, width=60)
key_schema_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Attribute Definitions (JSON):").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
attribute_definitions_entry = tk.Entry(root, width=60)
attribute_definitions_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Provisioned Throughput (JSON):").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
provisioned_throughput_entry = tk.Entry(root, width=60)
provisioned_throughput_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Button(root, text="Execute", command=handle_action).grid(row=5, column=0, columnspan=2, pady=10)

output_text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
output_text_area.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
