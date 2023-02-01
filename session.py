class Session:
    def __init__(self):
        self.players = {}

    def _check_name(self, player_name: str) -> bool:
        """
        Check if name already in session
        :param player_name:
        :return:
        """
        is_valid = True
        for player in self.players.keys():
            if player.lower() == player_name.lower():
                is_valid = False
                break

        return is_valid

    def _generate_index(self, player_name: str) -> int or None:
        """
        Generate player index
        :param player_name:
        :return:
        """
        if self._check_name(player_name):
            player_index = len(self.players.keys()) + 1
            self.players.update({player_name: player_index})
            return player_index
        else:
            return

    def add(self, player_name):
        if self._generate_index(player_name):
            return f'Player {player_name} added in session.'
        else:
            return f'Player {player_name} already in session.'

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



