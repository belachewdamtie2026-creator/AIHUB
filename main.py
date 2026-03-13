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
from kivy.utils import platform

import webbrowser
import os

Window.clearcolor = (0.08,0.08,0.08,1)

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


class CircularImage(Widget):

    def __init__(self, source, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None,None)
        self.size = (200,200)

        with self.canvas:
            self.ellipse = Ellipse(source=source,pos=self.pos,size=self.size)

        self.bind(pos=self.update,size=self.update)

    def update(self,*args):
        self.ellipse.pos=self.pos
        self.ellipse.size=self.size


class AIHub(App):

    def build(self):

        main = BoxLayout(orientation='vertical',padding=10,spacing=10)

        title = Label(
            text="AI HUB",
            font_size=32,
            size_hint=(1,0.12),
            color=(1,1,1,1)
        )

        self.search = TextInput(
            hint_text="Search AI tools...",
            size_hint=(1,0.1),
            multiline=False,
            background_color=(0.15,0.15,0.15,1),
            foreground_color=(1,1,1,1)
        )

        self.search.bind(text=self.update_search)

        about_btn = Button(
            text="About Developer",
            size_hint=(1,0.08),
            background_color=(0.3,0.6,0.3,1)
        )

        about_btn.bind(on_press=self.show_about)

        scroll = ScrollView()

        self.grid = GridLayout(
            cols=2,
            spacing=15,
            size_hint_y=None
        )

        self.grid.bind(minimum_height=self.grid.setter('height'))

        self.buttons=[]

        for name,url in AI_PLATFORMS:

            btn = Button(
                text=name,
                size_hint_y=None,
                height=160,
                background_color=(0.2,0.4,0.8,1),
                color=(1,1,1,1)
            )

            btn.bind(on_press=lambda x,u=url:self.open_link(u))

            self.grid.add_widget(btn)

            self.buttons.append((name,btn))

        scroll.add_widget(self.grid)

        main.add_widget(title)
        main.add_widget(self.search)
        main.add_widget(about_btn)
        main.add_widget(scroll)

        return main


    def open_link(self,url):

        if platform == "android":
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')

            intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
            currentActivity = PythonActivity.mActivity
            currentActivity.startActivity(intent)

        else:
            webbrowser.open(url)


    def update_search(self,instance,value):

        self.grid.clear_widgets()

        for name,url in AI_PLATFORMS:

            if value.lower() in name.lower():

                btn = Button(
                    text=name,
                    size_hint_y=None,
                    height=160,
                    background_color=(0.2,0.4,0.8,1),
                    color=(1,1,1,1)
                )

                btn.bind(on_press=lambda x,u=url:self.open_link(u))

                self.grid.add_widget(btn)


    def show_about(self,instance):

        layout = BoxLayout(
            orientation='vertical',
            padding=10,
            spacing=10
        )

        image_path = os.path.join("assets","belachew.jpg")

        circular_img = CircularImage(image_path)

        text = Label(
            text="""
AI HUB

Developed by:
Belachew Damtie

Student of Geospatial Analytics
and Remote Sensing

Bahir Dar University

This application provides
multiple AI platforms
in one place.
""",
            color=(1,1,1,1)
        )

        layout.add_widget(circular_img)
        layout.add_widget(text)

        popup = Popup(
            title="About Developer",
            content=layout,
            size_hint=(0.9,0.9)
        )

        popup.open()


if __name__ == "__main__":
    AIHub().run()