import smtplib
from email.message import EmailMessage
import tkinter as tk
from tkinter import messagebox, font, filedialog
from tkinter import PhotoImage
import json

def send_email(subject, body, to_email):
    from_email = 'nannurathore279@gmail.com'
    password = 'PUT APP PASSWORD HERE'

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
        return False

def send_bulk_emails(subject, body, emails):
    success = True
    for email in emails:
        if not send_email(subject, body, email):
            success = False
    return success

def load_emails_from_json():
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        try:
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                emails = data.get("emails", [])
                return emails
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load emails from file. Error: {e}")
    return []

def show_email_dialog():
    def update_fields():
        mode = mode_var.get()
        if mode == "single":
            recipient_label.config(text="Recipient Email:")
            recipient_entry.grid(row=3, column=1, padx=20, pady=10, sticky='ew')
            add_email_button.grid_forget()
            manual_emails.grid_forget()
            file_button.grid_forget()
        elif mode == "bulk":
            recipient_label.config(text="Recipient Emails:")
            recipient_entry.grid(row=3, column=1, padx=20, pady=10, sticky='ew')
            add_email_button.grid(row=3, column=2, padx=10, pady=10, sticky='ew')
            manual_emails.grid(row=4, column=1, padx=20, pady=10, sticky='ew')
            file_button.grid(row=5, column=1, padx=20, pady=10, sticky='ew')

    def on_submit():
        subject = subject_entry.get()
        body = body_text.get("1.0", tk.END).strip()
        mode = mode_var.get()

        if subject and body:
            if mode == "single":
                to_email = recipient_entry.get()
                if to_email:
                    success = send_email(subject, body, to_email)
                    if success:
                        messagebox.showinfo("Success", "Email sent successfully!")
                    else:
                        messagebox.showerror("Error", "Failed to send email.")
                else:
                    messagebox.showwarning("Warning", "Recipient email is required!")
            elif mode == "bulk":
                if bulk_emails_option_var.get() == "manual":
                    emails = manual_emails.get().split(';')
                    if emails:
                        success = send_bulk_emails(subject, body, emails)
                        if success:
                            messagebox.showinfo("Success", "Emails sent successfully!")
                        else:
                            messagebox.showerror("Error", "Failed to send some emails.")
                    else:
                        messagebox.showwarning("Warning", "No email addresses provided!")
                elif bulk_emails_option_var.get() == "file":
                    emails = load_emails_from_json()
                    if emails:
                        manual_emails.delete(0, tk.END)
                        manual_emails.insert(0, ';'.join(emails))
                        success = send_bulk_emails(subject, body, emails)
                        if success:
                            messagebox.showinfo("Success", "Emails sent successfully!")
                        else:
                            messagebox.showerror("Error", "Failed to send some emails.")
                    else:
                        messagebox.showwarning("Warning", "No emails loaded from file!")

        else:
            messagebox.showwarning("Warning", "All fields are required!")

    def on_hover(event):
        send_button.config(bg='#45A049', fg='#ffffff')  # Slightly darker green with white text

    def on_leave(event):
        send_button.config(bg='#4CAF50', fg='#ffffff')  # Original green with white text

    def add_email():
        current_emails = manual_emails.get()
        new_email = recipient_entry.get()
        if new_email:
            if current_emails:
                manual_emails.delete(0, tk.END)
                manual_emails.insert(0, current_emails + ";" + new_email)
            else:
                manual_emails.insert(0, new_email)
            recipient_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "No email address provided!")

    def show_help():
        help_text = (
            "This application allows you to send emails.\n\n"
            "1. Select 'Single Email' or 'Bulk Email' mode.\n\n"
            "For Single Email:\n"
            "2. Enter the subject of the email in the 'Subject' field.\n"
            "3. Type the content of the email in the 'Body' field.\n"
            "4. Enter the recipient's email address in the 'Recipient Email' field.\n"
            "5. Click 'Send Email' to send the email.\n\n"
            "For Bulk Email:\n"
            "6. Choose between 'Manual' or 'From File' for recipient emails.\n"
            "7. If 'Manual' is selected, enter multiple email addresses separated by semicolons.\n"
            "8. If 'From File' is selected, load the email addresses from a JSON file.\n"
            "9. Click 'Send Email' to send the emails.\n\n"
            "If you encounter any issues, check the console for error messages."
        )
        messagebox.showinfo("Help", help_text)

    root = tk.Tk()
    root.withdraw()

    dialog = tk.Toplevel(root)
    dialog.title("Send Email")

    # Maximize the window
    #dialog.state('zoomed')

    dialog.config(bg='#f2f2f2')  # Light gray background

    # Set icon (path needs to be adjusted to your icon file)
    try:
        icon = PhotoImage(file=r"C:\Users\Nannu\Desktop\soft\MENU\assets\t1.png")
        dialog.iconphoto(True, icon)
    except tk.TclError:
        print("Icon file not found.")

    custom_font = font.Font(family="Arial", size=12)
    label_color = '#333'  # Dark gray
    entry_color = '#fff'  # White
    button_color = '#4CAF50'  # Green
    button_text_color = '#fff'  # White

    mode_var = tk.StringVar(value="single")
    bulk_emails_option_var = tk.StringVar(value="manual")

    tk.Label(dialog, text="Mode:", font=custom_font, bg='#f2f2f2', fg=label_color).grid(row=0, column=0, padx=20, pady=10, sticky='w')
    tk.Radiobutton(dialog, text="Single Email", variable=mode_var, value="single", font=custom_font, bg='#f2f2f2', command=update_fields).grid(row=0, column=1, padx=20, pady=10, sticky='w')
    tk.Radiobutton(dialog, text="Bulk Email", variable=mode_var, value="bulk", font=custom_font, bg='#f2f2f2', command=update_fields).grid(row=0, column=2, padx=20, pady=10, sticky='w')

    tk.Label(dialog, text="Subject:", font=custom_font, bg='#f2f2f2', fg=label_color).grid(row=1, column=0, padx=20, pady=10, sticky='w')
    subject_entry = tk.Entry(dialog, font=custom_font, bg=entry_color)
    subject_entry.grid(row=1, column=1, padx=20, pady=10, sticky='ew')

    tk.Label(dialog, text="Body:", font=custom_font, bg='#f2f2f2', fg=label_color).grid(row=2, column=0, padx=20, pady=10, sticky='nw')
    body_text = tk.Text(dialog, font=custom_font, bg=entry_color)
    body_text.grid(row=2, column=1, padx=20, pady=10, sticky='nsew')

    recipient_label = tk.Label(dialog, text="Recipient Email:", font=custom_font, bg='#f2f2f2', fg=label_color)
    recipient_label.grid(row=3, column=0, padx=20, pady=10, sticky='w')

    recipient_entry = tk.Entry(dialog, font=custom_font, bg=entry_color)
    recipient_entry.grid(row=3, column=1, padx=20, pady=10, sticky='ew')

    add_email_button = tk.Button(dialog, text="Add Email", command=add_email, font=custom_font, bg=button_color, fg=button_text_color)
    add_email_button.grid(row=3, column=2, padx=10, pady=10, sticky='ew')

    manual_emails = tk.Entry(dialog, font=custom_font, bg=entry_color)
    manual_emails.grid(row=4, column=1, padx=20, pady=10, sticky='ew')

    file_button = tk.Button(dialog, text="Load Emails from File", command=lambda: manual_emails.insert(0, ';'.join(load_emails_from_json())), font=custom_font, bg=button_color, fg=button_text_color)
    file_button.grid(row=5, column=1, padx=20, pady=10, sticky='ew')

    send_button = tk.Button(dialog, text="Send Email", command=on_submit, font=custom_font, bg=button_color, fg=button_text_color)
    send_button.grid(row=6, column=1, padx=20, pady=20, sticky='ew')
    send_button.bind("<Enter>", on_hover)
    send_button.bind("<Leave>", on_leave)

    help_button = tk.Button(dialog, text="Help", command=show_help, font=custom_font, bg=button_color, fg=button_text_color)
    help_button.grid(row=6, column=0, padx=20, pady=20, sticky='ew')

    update_fields()  # Initialize fields based on default mode

    dialog.mainloop()

# Call the function to show the dialog
show_email_dialog()
