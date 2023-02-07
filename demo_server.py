from flask import Flask
from session import Session
from game import Game
from components import Item
app = Flask(__name__)
session = Session()
game = Game()
# <pass>


@app.route('/login/<user_name>')
def login(user_name):
    # user = request.args.get('user', type=str)
    # destination = request.args.get('url', type=str)
    player = session.add(user_name)
    print(player, 'Added in session')
    return str(game.add_player(player))


@app.route('/draw/<user_name>')
def draw(user_name):
    # user = request.args.get('user', type=str)
    # destination = request.args.get('url', type=str)
    # print(user_name, session.players.get(user_name))
    # print('SESSION', session.players)
    # print(session.validate(user_name))
    if session.validate(user_name):
        player = game.search_by_name(user_name)
        card = game.draw_card(player)
        player.add_item(card)
        return f'{str(player.name)} got {str(card)}'
    else:
        return f'User {user_name} not in session.'


@app.route('/inventory/<user_name>')
def inventory(user_name):
    # user = request.args.get('user', type=str)
    # destination = request.args.get('url', type=str)
    # print(user_name, session.players.get(user_name))
    # print('SESSION', session.players)
    # print(session.validate(user_name))
    print(session.players)
    if session.validate(user_name):
        player = game.search_by_name(user_name)
        print(str(player))
        return player.get_inventory()
    else:
        return f'User {user_name} not in session.'


@app.route('/synchronize')
def sync():
    # user = request.args.get('user', type=str)
    # destination = request.args.get('url', type=str)
    lst = []
    for player in game.players:
        lst.append(player.name)
    return {'players': lst}


@app.route('/start')
def start():
    # user = request.args.get('user', type=str)
    # destination = request.args.get('url', type=str)
    for player in game.players:
        for _ in range(5):
            player.add_item(Item('Item test', 1, 'credit', 'unk', '9999'))
    return game.__build_pool__()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4004)
