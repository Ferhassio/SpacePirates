import random
from game import Game
from player import Player

import kivy.uix.button as kb
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.lang import Builder
from content.src import *

Builder.load_file("Background.kv")
Window.size = (800, 600)

kv = '''
BoxLayoutWithPopup:
    orientation:'horizontal'
    spacing:10
    padding:5
    Button:
        text: 'Press me'
        size_hint:.3,.3
        on_press:
            root.pop1()
'''


# class CardPop(Widget):
#     def pop(self):
#         pop = Popup(title='Card', content=Image(source=VORTEX_PATH),
#                     size_hint=(None, None), size=(200, 300))
#         pop.open()

new_game = Game()


class Background(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(DrawBtn())
        self.add_widget(BuildBtn())
        self.add_widget(AddPlayer())


class DrawBtn(Widget):
    def __init__(self, **kwargs):
        super(DrawBtn, self).__init__(**kwargs)
        btn = kb.Button(text='Draw', size=(100, 40), pos=(0, 0))
        btn.bind(on_press=self.callback)
        self.add_widget(btn)

    def callback(self, instance):
        c = random.randint(1,100)
        player = new_game.players[0]
        print(player)
        item = new_game.draw_card(player)
        # print('itm', item)
        print(f'[{instance.state}] Draw a card "{c}"')
        pop = Popup(title=f'[#{item.item_id}] {item.name}', content=Image(source=VORTEX_PATH),
                    size_hint=(None, None), size=(200, 300))
        pop.open()
        # print('The button %s state is <%s>' % (instance, instance.state))


class BuildBtn(Widget):
    def __init__(self, **kwargs):
        super(BuildBtn, self).__init__(**kwargs)
        btn1 = kb.Button(text='Charge', size=(100, 40), pos=(100, 0))
        btn1.bind(on_press=self.callback)
        self.add_widget(btn1)

    def callback(self, instance):
        print('Pressed Charge', instance.state)


class AddPlayer(Widget):
    def __init__(self, **kwargs):
        super(AddPlayer, self).__init__(**kwargs)
        btn1 = kb.Button(text='Add Player', size=(100, 40), pos=(220, 0))
        btn1.bind(on_press=self.callback)
        self.add_widget(btn1)

    def callback(self, instance):
        player = new_game.add_player(Player('Politol', 1))
        new_game.__build_pool__()

        pop = Popup(title=f'Player {player.name} added!', content=Image(source=PLACEHOLDER),
                    size_hint=(None, None), size=(200, 300))
        pop.open()


class SpaceApp(App):
    def build(self):
        return Background()


if __name__ == '__main__':
    runTouchApp(SpaceApp().run())
