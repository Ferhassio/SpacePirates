import os
import re
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from content.src import PLACEHOLDER

Window.size = (600, 400)


class MyGridLayout(GridLayout):
    # Initialize infinite keywords
    def __init__(self, **kwargs):
        # Call grid layout constructor
        super(MyGridLayout, self).__init__(**kwargs)

        # Set columns
        self.cols = 2

        # Add widgets
        self.add_widget(Label(text="Your Nickname: "))
        # Add Input Box
        self.name = TextInput(multiline=False)
        self.add_widget(self.name)

        self.add_widget(Label(text="Server address (localhost default): "))
        # Add Input Box
        self.host = TextInput(multiline=False, text='localhost')
        self.add_widget(self.host)

        self.add_widget(Label(text="Server port (4004 default): "))
        # Add Input Box
        self.port = TextInput(multiline=False, text='4004')
        self.add_widget(self.port)

        # Create a Submit Button
        self.submit = Button(text="Run", font_size=32)
        # Bind the button
        self.submit.bind(on_press=self.press)
        self.add_widget(self.submit)

    def press(self, instance):
        name = self.name.text
        server = self.host.text
        port = self.port.text

        if len(name) < 3 or len(name) > 10:
            pop = Popup(title=f'Nickname {name} incorrect. Symbol limit is 3 to 10.', content=Image(source=PLACEHOLDER),
                        size_hint=(None, None), size=(200, 300))
            pop.open()

        elif server != 'localhost':
            if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", server):
                pop = Popup(title=f'Host {server} incorrect. Check spelling and dots.',
                            content=Image(source=PLACEHOLDER),
                            size_hint=(None, None), size=(200, 300))
                pop.open()

        # elif len(port) >= 1:
        #     try:
        #         port = int(port)
        #     except ValueError:
        #         pop = Popup(title=f'Port {port} incorrect. Use only integers.',
        #                     content=Image(source=PLACEHOLDER),
        #                     size_hint=(None, None), size=(200, 300))
        #         pop.open()
        else:
            os.system(f'start cmd /k python app.py {name} {server} {port}')
            Window.close()
            exit(f"Connection complete!")


class MyApp(App):
    def build(self):
        return MyGridLayout()


if __name__ == '__main__':
    MyApp().run()
