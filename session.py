from player import Player


class Session:
    def __init__(self):
        self.players = {}

    def validate(self, player_name: str) -> bool:
        """
        Check if name already in session
        :param player_name:
        :return:
        """
        is_valid = False
        for player in self.players.keys():
            if player.lower() == player_name.lower():
                is_valid = True
                break

        return is_valid

    def _generate_index(self, player_name: str) -> int or None:
        """
        Generate player index
        :param player_name:
        :return:
        """
        if not self.validate(player_name):
            player_index = len(self.players.keys()) + 1
            player = Player(player_name, player_index)
            self.players.update({player_name: player})

            return player
        else:
            return

    def add(self, player_name):
        player = self._generate_index(player_name)
        if player:
            return player
        else:
            return f'Player {player_name} already in session.'

    def remove(self, player_name):
        if player_name is self.players.keys():
            self.players.pop(player_name)
            return f'Player {player_name} Removed from session'
        else:
            return f'Player {player_name} not in session'

    def get_player(self, player_name):
        if self.validate(player_name):
            return self.players.get(player_name)
        else:
            return

    def close(self):
        self.players.clear()

    def __str__(self):
        return f'Current players: {self.players}'

    def __del__(self):
        self.close()


if __name__ == '__main__':
    new_session = Session()
    while True:
        name = input('Select name:')
        new_session.add(name)
        print(str(new_session), '\n')



