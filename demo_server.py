from flask import Flask
from session import Session
from game import Game
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
        return str(game.draw_card(session.get_player(user_name)))
    else:
        return f'User {user_name} not in session.'


@app.route('/start')
def start():
    # user = request.args.get('user', type=str)
    # destination = request.args.get('url', type=str)

    return game.__build_pool__()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4004)
