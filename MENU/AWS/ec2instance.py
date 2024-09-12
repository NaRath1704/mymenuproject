from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
import boto3
from botocore.exceptions import ClientError
import json

def read_aws_keys(filename):
    with open(filename, 'r') as file:
        keys = json.load(file)
    return keys

def launch_aws_instance(instance_type, image_id, region_name, aws_access_key, aws_secret_key, instance_name):
    ec2 = boto3.client(
        'ec2',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region_name
    )
    
    try:
        response = ec2.run_instances(
            InstanceType=instance_type,
            ImageId=image_id,
            MinCount=1,
            MaxCount=1,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': instance_name
                    }
                ]
            }]
        )
        instance_id = response['Instances'][0]['InstanceId']
        return {"success": True, "instance_id": instance_id}
    except ClientError as e:
        return {"success": False, "error": str(e)}

class AWSInstanceLauncherApp(App):
    def build(self):
        # Set window icon
        try:
            Window.set_icon(r'MENU\assets\EC2.png')
        except Exception as e:
            print(f"Icon setting error: {e}")

        # Set window size (width, height)
        Window.size = (900, 400)  # Increased width by 1/2

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Title
        title_label = Label(
            text='AWS Instance Launcher', 
            font_size=24, 
            bold=True, 
            size_hint_y=None, 
            height=40
        )
        layout.add_widget(title_label)

        # Input fields
        input_layout = BoxLayout(orientation='vertical', spacing=10)

        # Instance type
        self.instance_type_input = self.create_input_field('Instance Type:', 't2.micro')
        input_layout.add_widget(self.instance_type_input)

        # Image ID
        self.image_id_input = self.create_input_field('Image ID:', 'ami-02b49a24cfb95941c')
        input_layout.add_widget(self.image_id_input)

        # Region name
        self.region_name_input = self.create_input_field('Region Name:', 'ap-south-1')
        input_layout.add_widget(self.region_name_input)

        # Instance name
        self.instance_name_input = self.create_input_field('Instance Name:', '')
        input_layout.add_widget(self.instance_name_input)

        layout.add_widget(input_layout)

        # Submit button
        submit_button = Button(text='Launch Instance', size_hint_y=None, height=50)
        submit_button.bind(on_press=self.launch_instance)
        layout.add_widget(submit_button)

        return layout

    def create_input_field(self, label_text, default_text):
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        label = Label(text=label_text, size_hint_x=None, width=150)
        text_input = TextInput(text=default_text, multiline=False, hint_text=f'Enter {label_text.lower()}')
        text_input.padding_y = [10, 5]  # Add padding to the bottom
        box.add_widget(label)
        box.add_widget(text_input)
        return box

    def launch_instance(self, instance):
        # Read AWS credentials from JSON file
        keys = read_aws_keys(r'MENU\AWS\aws_credentials.json')
        aws_access_key = keys.get('aws_access_key_id')
        aws_secret_key = keys.get('aws_secret_access_key')

        if not aws_access_key or not aws_secret_key:
            self.show_popup('Error', 'AWS keys are missing from the credentials file.')
            return

        # Get inputs
        instance_type = self.instance_type_input.children[0].text
        image_id = self.image_id_input.children[0].text
        region_name = self.region_name_input.children[0].text
        instance_name = self.instance_name_input.children[0].text

        result = launch_aws_instance(instance_type, image_id, region_name, aws_access_key, aws_secret_key, instance_name)

        if result.get('success'):
            self.show_popup('Success', f'Instance launched successfully! Instance ID: {result["instance_id"]}', success=True)
        else:
            self.show_popup('Error', f'Error launching instance: {result["error"]}')

    def show_popup(self, title, message, success=False):
        # Create layout for the popup
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        message_label = Label(text=message, size_hint_y=None, height=40, color=(0, 1, 0, 1) if success else (1, 0, 0, 1))
        ok_button = Button(text='OK', size_hint_y=None, height=50)

        # Bind button to close the app
        ok_button.bind(on_press=self.close_app if success else lambda x: self.popup.dismiss())

        content.add_widget(message_label)
        content.add_widget(ok_button)

        # Double the width for success messages
        popup_width = 800 if success else 400

        self.popup = Popup(title=title, content=content, size_hint=(None, None), size=(popup_width, 200))
        self.popup.open()

    def close_app(self, instance):
        self.stop()

if __name__ == '__main__':
    AWSInstanceLauncherApp().run()
