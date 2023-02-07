import argparse
import random
import socket

import requests
from kivy.properties import StringProperty, Clock
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from game import Game
from player import Player
import kivy.uix.button as kb
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window, Animation
from kivy.app import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.lang import Builder
from content.src import *
from client import Client

Builder.load_file("Background.kv")
Window.size = (800, 600)

new_game = Game()

global MESSAGE


class MoveableImage(Image):

    def __init__(self, **kwargs):
        super(MoveableImage, self).__init__(**kwargs)
        self.x -= random.randint(1, 1000)
        self.y -= random.randint(1, 1000)

        self.x += random.randint(1, 1000)
        self.y += random.randint(1, 1000)


# class ServerMessage(Label):
#     # message = StringProperty()
#
#     def __init__(self, **kwargs):
#         super(ServerMessage, self).__init__(**kwargs)
#         self.text = 'Connecting...'
#         self.color = 'red'
#         self.font_size = '20sp'
#         self.pos = (300, 0)
#         Clock.schedule_interval(self.update, 5)
#
#     def update(self, instance):
#         self.text += MESSSAGE if MESSSAGE else 'Server is down.'

class ServerMessage(TextInput):
    def __init__(self, **kwargs):
        super(ServerMessage, self).__init__(**kwargs)
        self.multiline = True
        self.text = 'Server messages'
        Clock.schedule_interval(self.callback, 1)

    def callback(self, instance):
        if self.text.split('\n')[-1] != MESSAGE:
            self.text += '\n' + MESSAGE
            print(self.text)
            print()



class Background(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # wimg = MoveableImage(source=VORTEX_PATH)
        img = Image(source=VORTEX_PATH)
        self.add_widget(DrawBtn())
        self.add_widget(BuildBtn())
        self.add_widget(Buy())
        self.add_widget(img)
        self.add_widget(ServerMessage())


    def animate(self, instance):
        # create an animation object. This object could be stored
        # and reused each call or reused across different widgets.
        # += is a sequential step, while &= is in parallel
        animation = Animation(pos=(100, 100), t='out_bounce')
        animation += Animation(pos=(200, 100), t='out_bounce')
        animation &= Animation(size=(500, 500))
        animation += Animation(size=(100, 50))

        # apply the animation on the button, passed in the "instance" argument
        # Notice that default 'click' animation (changing the button
        # color while the mouse is down) is unchanged.
        animation.start(instance)


class DrawBtn(Widget):
    def __init__(self, **kwargs):
        super(DrawBtn, self).__init__(**kwargs)
        btn = kb.Button(text='Draw', size=(100, 40), pos=(0, 120))
        btn.bind(on_press=self.callback)
        self.add_widget(btn)

    def callback(self, instance):
        resp = requests.get(f'http://{HOST}:{PORT}/draw/{player_name}')
        # c = random.randint(1, 100)
        # player = new_game.players[0]
        # print(player)
        # item = new_game.draw_card(player)
        # # print('itm', item)
        # print(f'[{instance.state}] Draw a card "{c}"')
        # pop = Popup(title=f'[#{item.item_id}] {item.name}', content=Image(source=VORTEX_PATH),
        #             size_hint=(None, None), size=(200, 300))
        # pop.open()
        global MESSAGE
        MESSAGE = player_name + ' got ' + resp.text
        pop = Popup(title=resp.text, content=Image(source=VORTEX_PATH),
                    size_hint=(None, None), size=(200, 300))
        pop.open()

        # print('The button %s state is <%s>' % (instance, instance.state))


class BuildBtn(Widget):
    def __init__(self, **kwargs):
        super(BuildBtn, self).__init__(**kwargs)
        btn1 = kb.Button(text='Charge', size=(100, 40), pos=(100, 120))
        btn1.bind(on_press=self.callback)
        self.add_widget(btn1)

    def callback(self, instance):
        print('Pressed Charge', instance.state)


class Buy(Widget):
    def __init__(self, **kwargs):
        super(Buy, self).__init__(**kwargs)
        btn1 = kb.Button(text='Buy', size=(100, 40), pos=(200, 120))
        btn1.bind(on_press=self.callback)
        self.add_widget(btn1)

    def callback(self, instance):
        pass
        # player = new_game.add_player(Player('Politol', 1))
        # new_game.__build_pool__()

        # pop = Popup(title=f'Player {player.name} added!', content=Image(source=PLACEHOLDER),
        #             size_hint=(None, None), size=(200, 300))
        # pop.open()


class SpaceApp(App):
    def build(self):
        global MESSAGE
        MESSAGE = requests.get(f'http://{HOST}:{PORT}/start').text
        return Background()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set server config.')
    parser.add_argument('pname', type=str, help='Host')
    parser.add_argument('host', type=str, help='Host')
    parser.add_argument('port', type=str, help='True for update mode, False for search mode')

    args = parser.parse_args()

    player_name = args.pname
    HOST = args.host
    PORT = args.port
    try:
        global MESSAGE
        resp = requests.get(f'http://{HOST}:{PORT}/login/{player_name}')
        print('Connected', resp.text)
        if resp.status_code == 200:
            MESSAGE = resp.text
        else:
            MESSAGE = f'Request error [{resp.status_code}]. {resp.text}'
    except requests.exceptions.ConnectionError:
        MESSAGE = 'Server is down.'

    # game_session = Client(HOST, PORT, player_name)
    runTouchApp(SpaceApp().run())
