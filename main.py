from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse
from kivy.core.window import Window
import webbrowser
import sys
import os

# Mobile-friendly window background
Window.clearcolor = (0.08, 0.08, 0.08, 1)

# AI Platforms list
AI_PLATFORMS = [
    ("ChatGPT","https://chat.openai.com"),
    ("Gemini","https://gemini.google.com"),
    ("Claude","https://claude.ai"),
    ("Perplexity","https://www.perplexity.ai"),
    ("Copilot","https://copilot.microsoft.com"),
    ("Grammarly","https://grammarly.com"),
    ("QuillBot","https://quillbot.com"),
    ("Replit","https://replit.com"),
    ("Midjourney","https://www.midjourney.com"),
    ("Leonardo AI","https://leonardo.ai"),
    ("Poe AI","https://poe.com"),
    ("Character AI","https://character.ai"),
    ("HuggingChat","https://huggingface.co/chat"),
    ("You AI","https://you.com"),
    ("DeepAI","https://deepai.org")
]

# Circular Image Widget for About popup
class CircularImage(Widget):
    def __init__(self, source, **kwargs):
        super().__init__(**kwargs)
        self.source = source
        self.size_hint = (None, None)
        self.size = (200, 200)
        with self.canvas:
            self.ellipse = Ellipse(source=self.source, pos=self.pos, size=self.size)
        self.bind(pos=self.update_ellipse, size=self.update_ellipse)

    def update_ellipse(self, *args):
        self.ellipse.pos = self.pos
        self.ellipse.size = self.size

class AIHub(App):

    def build(self):
        self.current_index = 0
        self.buttons = []

        main = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Title
        title = Label(text="AI HUB", font_size=36, size_hint=(1,0.12), color=(1,1,1,1))

        # Search bar
        search = TextInput(hint_text="Search AI tools...", size_hint=(1,0.1), multiline=False,
                           background_color=(0.15,0.15,0.15,1), foreground_color=(1,1,1,1))
        search.bind(text=self.update_search)

        # About button
        about_btn = Button(text="About Developer", size_hint=(1,0.08), background_color=(0.3,0.6,0.3,1))
        about_btn.bind(on_press=self.show_about)

        # Scrollable grid of AI buttons
        scroll = ScrollView()
        self.grid = GridLayout(cols=2, spacing=15, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))

        for name, url in AI_PLATFORMS:
            btn = self.create_button(name, url)
            self.grid.add_widget(btn)
            self.buttons.append(btn)

        scroll.add_widget(self.grid)

        # Add to main layout
        main.add_widget(title)
        main.add_widget(search)
        main.add_widget(about_btn)
        main.add_widget(scroll)

        # Bind arrow keys
        Window.bind(on_key_down=self.on_key_down)

        # Highlight first button
        self.update_highlight()

        return main

    def create_button(self, name, url):
        btn = Button(text=name, size_hint_y=None, height=180,
                     background_color=(0.2,0.4,0.8,1), color=(1,1,1,1))
        btn.bind(on_press=lambda x: webbrowser.open(url))
        return btn

    def update_highlight(self):
        if not self.buttons:
            return
        for i, btn in enumerate(self.buttons):
            if i == self.current_index:
                btn.background_color = (1,0.6,0,1)
                # Scroll into view
                scroll_height = self.grid.parent.height
                scroll_y = 1 - (btn.y / max(self.grid.height - scroll_height, 1))
                scroll_y = min(max(scroll_y, 0), 1)
                self.grid.parent.scroll_y = scroll_y
            else:
                btn.background_color = (0.2,0.4,0.8,1)

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if not self.buttons:
            return
        cols = 2
        total = len(self.buttons)
        row = self.current_index // cols
        col = self.current_index % cols

        if key == 273:  # up
            row = max(0, row-1)
        elif key == 274:  # down
            row = min((total-1)//cols, row+1)
        elif key == 275:  # right
            col = min(cols-1, col+1)
        elif key == 276:  # left
            col = max(0, col-1)
        elif key == 13:  # Enter
            self.buttons[self.current_index].trigger_action(duration=0.1)
            return

        self.current_index = min(row*cols + col, total-1)
        self.update_highlight()

    def update_search(self, instance, value):
        self.grid.clear_widgets()
        self.buttons = []
        for name, url in AI_PLATFORMS:
            if value.lower() in name.lower():
                btn = self.create_button(name, url)
                self.grid.add_widget(btn)
                self.buttons.append(btn)
        self.current_index = 0
        self.update_highlight()

    def show_about(self, instance):
        content = ScrollView(size_hint=(1,1))
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Dynamic path for assets
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        image_path = os.path.join(base_path, "assets", "belachew.jpg")

        circular_img = CircularImage(image_path)

        about_text = Label(
            text="""
AI HUB

Developed by:
Belachew Damtie

Student of Geospatial Analytics
and Remote Sensing

Bahir Dar University

This application provides a hub
for accessing multiple AI platforms
in one place.
""",
            color=(1,1,1,1),
            size_hint=(1,None),
            height=300
        )

        layout.add_widget(circular_img)
        layout.add_widget(about_text)
        content.add_widget(layout)

        popup = Popup(title="About Developer", content=content, size_hint=(0.9,0.9))
        popup.open()

if __name__ == "__main__":
    AIHub().run()