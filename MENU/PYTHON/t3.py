from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.popup import Popup
import requests
from bs4 import BeautifulSoup
import webbrowser

# Set window background color
Window.clearcolor = (1, 1, 1, 1)  # Light background

class GoogleSearchApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Add search input
        self.search_input = TextInput(hint_text='Enter search query', size_hint_y=None, height=40)
        self.layout.add_widget(self.search_input)
        
        # Add result count input
        self.result_count_input = TextInput(hint_text='Number of results (5-20)', size_hint_y=None, height=40, input_filter='int')
        self.layout.add_widget(self.result_count_input)
        
        # Add search button
        search_button = Button(text='Search', size_hint_y=None, height=50)
        search_button.bind(on_press=self.perform_search)
        self.layout.add_widget(search_button)
        
        # Add scrollable result area
        self.result_area = ScrollView(size_hint=(1, 1))
        self.result_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
        self.result_layout.bind(minimum_height=self.result_layout.setter('height'))
        self.result_area.add_widget(self.result_layout)
        self.layout.add_widget(self.result_area)
        
        return self.layout

    def perform_search(self, instance):
        query = self.search_input.text
        result_count = self.result_count_input.text
        
        # Validate result count
        if result_count:
            try:
                result_count = int(result_count)
                if result_count < 5:
                    result_count = 5
                elif result_count > 20:
                    result_count = 20
            except ValueError:
                self.show_popup('Error', 'Invalid number of results. Using default value of 10.')
                result_count = 10
        else:
            result_count = 10
        
        if query:
            search_url = f'https://www.google.com/search?q={query}'
            try:
                response = requests.get(search_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                results = soup.find_all('a')
                
                # Clear previous results
                self.result_layout.clear_widgets()
                
                count = 0
                for result in results:
                    link = result.get('href')
                    # Filter out dead links
                    if link and link.startswith('/url?q='):
                        link = link[7:].split('&')[0]
                        if "maps.google.com" in link or "ved=1t:" in link or link.startswith("/search"):
                            continue  # Skip dead links
                        self.add_link(link)
                        count += 1
                        if count >= result_count:
                            break
            
            except requests.RequestException as e:
                self.show_popup('Error', f'Error fetching search results: {e}')
    
    def add_link(self, url):
        link_label = Label(text=url, color=(0, 0, 1, 1), size_hint_y=None, height=30)
        link_label.bind(on_touch_down=lambda instance, touch: self.open_link(instance, touch, url))
        self.result_layout.add_widget(link_label)
    
    def open_link(self, instance, touch, url):
        if instance.collide_point(*touch.pos):
            webbrowser.open(url)

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        close_button = Button(text='Close', size_hint_y=None, height=40)
        close_button.bind(on_press=lambda x: self.popup.dismiss())
        content.add_widget(close_button)
        self.popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        self.popup.open()

if __name__ == '__main__':
    GoogleSearchApp().run()
