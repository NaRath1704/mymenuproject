import uiautomator2 as u2
import time

# Connect to the device
d = u2.connect()

def add_contact(name, phone):
    d.screen_on()
    d.press("home")

    # Open the Phone app
    d(description="Phone").click()

    # Wait for the Phone app to open and go to Contacts
    d(text="Contacts").wait(timeout=10)
    d(text="Contacts").click()

    # Click on "Create new contact" button using resource ID
    d(resourceId="com.google.android.dialer:id/contact_name").click()

    # Wait for the contact creation screen
    d(resourceId="com.google.android.contacts:id/editor_title").wait(timeout=10)

    # Tap on the "First name" field to focus
    d(className="android.widget.EditText", text="First name").click()
    # Enter the name with "Learner LW" prefix
    d(className="android.widget.EditText", text="First name").set_text(f"Learner LW {name}")
    
    d.press("back")

    # Tap on the "Phone" field to focus
    d(className="android.widget.EditText", text="Phone").click()
    # Enter the phone number
    d(className="android.widget.EditText", text="Phone").set_text(phone)

    # Tap on the "Save" button
    d(resourceId="com.google.android.contacts:id/toolbar_button").click()

    print(f"Contact '{name}' with phone number '{phone}' added.")

# List of contacts
contacts = [
    {"name": "Afsar Ali", "phone": "8189877423"},
    {"name": "Anurag Sandesh Bibave", "phone": "9607375177"},
    {"name": "Chandrakant Mahadeshwar", "phone": "9049271713"},
    {"name": "Goutham", "phone": "9491415555"},
    {"name": "Inturi Manasa", "phone": "7661866628"},
    {"name": "K Suman", "phone": "8520005318"},
    {"name": "NAIDU HARI NADH", "phone": "9966474961"},
    {"name": "Nilesh Pasarate", "phone": "8806937400"},
    {"name": "Prabhakaran G", "phone": "9791044244"},
    {"name": "Pradeep Arora", "phone": "9214931264"},
    {"name": "Ravi kumar sharma", "phone": "7737177121"},
    {"name": "SANAT KUMAR NAYAK", "phone": "7064736067"},
    {"name": "Sachin Dawre", "phone": "8108317191"},
    {"name": "Shuchi Vijay", "phone": "9560707398"},
    {"name": "Thiyagarajan Chandran", "phone": "9731188885"},
    {"name": "Tribhawan Singh", "phone": "918237067471"},
    {"name": "Upmanyu Sharma", "phone": "7889774471"},
    {"name": "Yogesh Kancherla", "phone": "9000421473"},
    {"name": "Yogesh Kumar Prajapati", "phone": "8770974677"}
]

# Add each contact
for contact in contacts:
    add_contact(contact["name"], contact["phone"])
    time.sleep(1)  # Adding a delay to ensure each contact is saved properly before the next one
