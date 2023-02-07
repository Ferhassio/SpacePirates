import argparse
import random
import socket
import time

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
global PLAYERS


class ServerMessage(TextInput):
    def __init__(self, **kwargs):
        super(ServerMessage, self).__init__(**kwargs)
        self.multiline = True
        self.text = 'Server messages'
        Clock.schedule_interval(self.callback, .5)

    def callback(self, instance):
        # print(self.text.split('\n')[-1], ' - - - ', MESSAGE)
        if self.text.split('\n')[-1] != MESSAGE:
            self.text += '\n' + MESSAGE


class Background(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(DrawBtn())
        self.add_widget(BuildBtn())
        self.add_widget(Buy())
        self.add_widget(Play())
        self.add_widget(ServerMessage())

        self.init_pool()
        self.load()

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

    def load(self):
        global MESSAGE
        response = requests.get(f'http://{HOST}:{PORT}/synchronize')

        print('Resp', response.json())
        players = response.json()['players']
        # self.remove_widget(Play())

        for player in players:
            print('Player', player)
            MESSAGE += '\n' + player + ' added.'
            self.add_widget(Ship(owner=player))

    def init_pool(self):
        global MESSAGE
        MESSAGE += '\n' + requests.get(f'http://{HOST}:{PORT}/start').text
        print('Pool inited', MESSAGE)


# class Sync(Widget):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#
#     def sync(self, instance):
#         global MESSAGE
#         response = requests.get(f'http://{HOST}:{PORT}/synchronize')
#         MESSAGE = response.text
#
#         print('Resp', response.json())
#         players = response.json()['players']
#
#         for player in players:
#             print('Player', player)
#             Ship.text = player
#             self.add_widget(Ship())


class Play(Widget):
    def __init__(self, **kwargs):
        super(Play, self).__init__(**kwargs)
        play_btn = kb.Button(text='Start Game', size=(100, 40), pos=(300, 120))
        play_btn.bind(on_press=self.callback)
        self.add_widget(play_btn)

    def callback(self, instance):
        global MESSAGE
        response = requests.get(f'http://{HOST}:{PORT}/start')
        MESSAGE = response.text
        self.disabled = False

        # DrawBtn.disabled = False
        # BuildBtn.disabled = False
        # Buy.disabled = False

        pop = Popup(title='Game started!', content=Image(source=PLACEHOLDER),
                    size_hint=(None, None), size=(200, 300))
        pop.open()


class Ship(Widget):
    owner = StringProperty()

    def __init__(self, **kwargs):
        super(Ship, self).__init__(**kwargs)
        ship_obj = kb.Button(pos=(random.randint(0, 400), random.randint(120, 500)),
                             background_normal=SHIP,
                             background_down=SHIP,
                             color='red',
                             text=self.owner)
        ship_obj.bind(on_press=self.callback)
        self.add_widget(ship_obj)

    def callback(self, instance):
        global MESSAGE
        response = requests.get(f'http://{HOST}:{PORT}/inventory/{self.owner}')
        MESSAGE = f'Inventory of {self.owner} opened by {player_name}!!'
        pop = Popup(title=f'{self.owner}`s inventory',
                    content=TextInput(text=response.text, multiline=True),
                    size_hint=(None, None), size=(200, 300))
        pop.open()


class DrawBtn(Widget):
    def __init__(self, **kwargs):
        super(DrawBtn, self).__init__(**kwargs)
        draw_btn = kb.Button(text='Draw', size=(100, 40), pos=(0, 120))
        draw_btn.bind(on_press=self.callback)
        self.add_widget(draw_btn)
        # self.disabled = True

    def callback(self, instance):
        response = requests.get(f'http://{HOST}:{PORT}/draw/{player_name}')

        global MESSAGE
        MESSAGE = player_name + ' got ' + response.text
        pop = Popup(title=response.text, content=Image(source=VORTEX_PATH),
                    size_hint=(None, None), size=(200, 300))
        pop.open()


class BuildBtn(Widget):
    def __init__(self, **kwargs):
        super(BuildBtn, self).__init__(**kwargs)
        build_btn = kb.Button(text='Charge', size=(100, 40), pos=(100, 120))
        build_btn.bind(on_press=self.callback)
        self.add_widget(build_btn)
        # self.disabled = True

    def callback(self, instance):
        print('Pressed Charge', instance.state)


class Buy(Widget):
    def __init__(self, **kwargs):
        super(Buy, self).__init__(**kwargs)
        btn1 = kb.Button(text='Buy', size=(100, 40), pos=(200, 120))
        btn1.bind(on_press=self.callback)
        self.add_widget(btn1)
        # self.disabled = True

    def callback(self, instance):
        global MESSAGE
        MESSAGE = 'Buy prototype button'


class SpaceApp(App):
    def build(self):
        if not server_state:
            Play.disabled = True

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
    server_state = True
    try:
        global MESSAGE
        resp = requests.get(f'http://{HOST}:{PORT}/login/{player_name}')
        print('Connected', resp.text)
        if resp.status_code == 200:
            MESSAGE = resp.text
        else:
            MESSAGE = f'Request error [{resp.status_code}]. {resp.text}'
            server_state = False
    except requests.exceptions.ConnectionError:
        MESSAGE = 'Server is down'
        server_state = False

    # game_session = Client(HOST, PORT, player_name)
    runTouchApp(SpaceApp().run())
