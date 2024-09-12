import tkinter as tk
from tkinter import scrolledtext, ttk
import subprocess
import threading
import time

class DockerApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Docker Automation")
        self.root.iconbitmap(r"MENU\assets\docker-svgrepo-com (2).ico")
        self.create_widgets()
        self.stop_live_update = True

    def create_widgets(self):
        # Create a Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Pulled Images Tab
        self.pulled_images_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.pulled_images_frame, text="Pulled Images")
        self.create_pulled_images_tab()

        # Container Management Tab
        self.container_management_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.container_management_frame, text="Container Management")
        self.create_container_management_tab()

        # Docker Volume and Network Tab
        self.docker_volume_network_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.docker_volume_network_frame, text="Docker Volume & Network")
        self.create_docker_volume_network_tab()

    def create_pulled_images_tab(self):
        # Title
        self.title_label = tk.Label(self.pulled_images_frame, text="Pulled Images", font=("Helvetica", 18))
        self.title_label.pack(pady=10)

        # Image Name Entry
        self.image_name_label = tk.Label(self.pulled_images_frame, text="Enter Image Name")
        self.image_name_label.pack(pady=5)

        self.image_name_entry = tk.Entry(self.pulled_images_frame, width=50)
        self.image_name_entry.pack(pady=5)

        # Buttons
        self.pull_image_button = tk.Button(self.pulled_images_frame, text="Pull Image", command=self.pull_image)
        self.pull_image_button.pack(side=tk.LEFT, padx=5)

        self.get_all_images_button = tk.Button(self.pulled_images_frame, text="Get All Images", command=self.get_all_images)
        self.get_all_images_button.pack(side=tk.LEFT, padx=5)

        self.show_running_containers_button = tk.Button(self.pulled_images_frame, text="Show Running Containers", command=self.get_all_running_containers)
        self.show_running_containers_button.pack(side=tk.LEFT, padx=5)

        self.show_all_containers_button = tk.Button(self.pulled_images_frame, text="Show All Containers", command=self.get_all_containers)
        self.show_all_containers_button.pack(side=tk.LEFT, padx=5)

        self.live_update_button = tk.Button(self.pulled_images_frame, text="Live Update", command=self.toggle_live_update)
        self.live_update_button.pack(side=tk.LEFT, padx=5)

        # Output Area
        self.output_text = scrolledtext.ScrolledText(self.pulled_images_frame, height=10, width=80)
        self.output_text.pack(pady=5)

        # Status Label
        self.status_label = tk.Label(self.pulled_images_frame, text="", font=("Helvetica", 12))
        self.status_label.pack(pady=5)

    def create_container_management_tab(self):
        # Launch Container
        self.launch_container_label = tk.Label(self.container_management_frame, text="Launch a Container", font=("Helvetica", 18))
        self.launch_container_label.pack(pady=10)

        self.container_name_label = tk.Label(self.container_management_frame, text="Enter Container Name")
        self.container_name_label.pack(pady=5)

        self.container_name_entry = tk.Entry(self.container_management_frame, width=50)
        self.container_name_entry.pack(pady=5)

        self.image_name_label = tk.Label(self.container_management_frame, text="Enter Image Name")
        self.image_name_label.pack(pady=5)

        self.image_name_entry = tk.Entry(self.container_management_frame, width=50)
        self.image_name_entry.pack(pady=5)

        self.launch_container_button = tk.Button(self.container_management_frame, text="Launch Container", command=self.launch_container)
        self.launch_container_button.pack(pady=5)

        # Start Container
        self.start_container_label = tk.Label(self.container_management_frame, text="Start Container", font=("Helvetica", 18))
        self.start_container_label.pack(pady=10)

        self.start_container_entry = tk.Entry(self.container_management_frame, width=50)
        self.start_container_entry.pack(pady=5)

        self.start_container_label = tk.Label(self.container_management_frame, text="Enter Container Name")
        self.start_container_label.pack(pady=5)

        self.start_container_button = tk.Button(self.container_management_frame, text="Start Container", command=self.start_container)
        self.start_container_button.pack(pady=5)

        # Stop Container
        self.stop_container_label = tk.Label(self.container_management_frame, text="Stop Container", font=("Helvetica", 18))
        self.stop_container_label.pack(pady=10)

        self.stop_container_entry = tk.Entry(self.container_management_frame, width=50)
        self.stop_container_entry.pack(pady=5)

        self.stop_container_label = tk.Label(self.container_management_frame, text="Enter Container Name")
        self.stop_container_label.pack(pady=5)

        self.stop_container_button = tk.Button(self.container_management_frame, text="Stop Container", command=self.stop_container)
        self.stop_container_button.pack(pady=5)

    def create_docker_volume_network_tab(self):
        # Docker Volume
        self.docker_volume_button = tk.Button(self.docker_volume_network_frame, text="List Docker Volume", command=self.dockervolume)
        self.docker_volume_button.pack(pady=10)

        # Docker Network
        self.docker_network_button = tk.Button(self.docker_volume_network_frame, text="List Docker Network", command=self.dockernetwork)
        self.docker_network_button.pack(pady=10)

    def run_command(self, cmd):
        try:
            # Use subprocess.Popen to handle real-time output
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = ""
            while True:
                line = process.stdout.readline()
                if line:
                    output += line
                    self.update_output_text(output)
                if process.poll() is not None:
                    break
            stderr = process.stderr.read()
            if stderr:
                output += stderr
                self.update_output_text(output)
            return output
        except Exception as e:
            return str(e)

    def pull_image(self):
        image_name = self.image_name_entry.get()
        if image_name:
            self.status_label.config(text="Pulling image...")
            self.root.update()
            cmd = f"docker pull {image_name}"
            threading.Thread(target=self.run_command, args=(cmd,)).start()
            self.notebook.select(self.pulled_images_frame)
        else:
            self.update_output_text("Please enter an image name.")
            self.status_label.config(text="")

    def get_all_images(self):
        self.status_label.config(text="Fetching images...")
        self.root.update()
        cmd = "docker images"
        threading.Thread(target=self.run_command, args=(cmd,)).start()
        self.notebook.select(self.pulled_images_frame)

    def get_all_running_containers(self):
        self.status_label.config(text="Fetching running containers...")
        self.root.update()
        cmd = "docker ps"
        threading.Thread(target=self.run_command, args=(cmd,)).start()
        self.notebook.select(self.pulled_images_frame)

    def get_all_containers(self):
        self.status_label.config(text="Fetching all containers...")
        self.root.update()
        cmd = "docker ps -a"
        threading.Thread(target=self.run_command, args=(cmd,)).start()
        self.notebook.select(self.pulled_images_frame)

    def launch_container(self):
        container_name = self.container_name_entry.get()
        image_name = self.image_name_entry.get()
        if container_name and image_name:
            self.status_label.config(text="Launching container...")
            self.root.update()
            cmd = f"docker run -dit --name {container_name} {image_name}"
            threading.Thread(target=self.run_command, args=(cmd,)).start()
            self.notebook.select(self.pulled_images_frame)
        else:
            self.update_output_text("Please enter both container and image names.")
            self.status_label.config(text="")

    def start_container(self):
        container_name = self.start_container_entry.get()
        if container_name:
            self.status_label.config(text="Starting container...")
            self.root.update()
            cmd = f"docker start {container_name}"
            threading.Thread(target=self.run_command, args=(cmd,)).start()
            self.notebook.select(self.pulled_images_frame)
        else:
            self.update_output_text("Please enter a container name.")
            self.status_label.config(text="")

    def stop_container(self):
        container_name = self.stop_container_entry.get()
        if container_name:
            self.status_label.config(text="Stopping container...")
            self.root.update()
            cmd = f"docker stop {container_name}"
            threading.Thread(target=self.run_command, args=(cmd,)).start()
            self.notebook.select(self.pulled_images_frame)
        else:
            self.update_output_text("Please enter a container name.")
            self.status_label.config(text="")

    def dockervolume(self):
        self.status_label.config(text="Fetching volumes...")
        self.root.update()
        cmd = "docker volume ls"
        threading.Thread(target=self.run_command, args=(cmd,)).start()
        self.notebook.select(self.pulled_images_frame)

    def dockernetwork(self):
        self.status_label.config(text="Fetching networks...")
        self.root.update()
        cmd = "docker network ls"
        threading.Thread(target=self.run_command, args=(cmd,)).start()
        self.notebook.select(self.pulled_images_frame)

    def toggle_live_update(self):
        if self.stop_live_update:
            self.stop_live_update = False
            self.live_update_thread = threading.Thread(target=self.live_update)
            self.live_update_thread.start()
            self.live_update_button.config(text="Stop Live Update")
        else:
            self.stop_live_update = True
            self.live_update_thread.join()
            self.live_update_button.config(text="Live Update")

    def live_update(self):
        while not self.stop_live_update:
            self.get_all_containers()
            time.sleep(5)

    def update_output_text(self, text):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text + '\n')

if __name__ == "__main__":
    root = tk.Tk()
    app = DockerApp(root)
    root.mainloop()
