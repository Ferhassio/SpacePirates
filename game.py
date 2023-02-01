import random
from operator import itemgetter

from components import Item, ItemPoolMaster
from player import Player
from random import shuffle


class Game:
    def __init__(self, players: list[Player]):
        self.default_items = [('credit', 50), ('robot', 20), ('pirate', 30)]
        self.ItemPoolGenerator = ItemPoolMaster(len(players), self.default_items)
        self.game_pool = self.ItemPoolGenerator.build_pool()

        self.players = players
        self.current_turn = 0

        self.pirate_draw = []
        self.robot_draw = []
        self.colors_in_game = {}

        self.game_state = None

        self.set_order()
        print('Game data loaded. Total items:', len(self.game_pool))

    def _check_robot_draw(self):


    def shuffle_pool(self):
        self.game_pool.extend(self.pirate_draw + self.robot_draw)

    def set_order(self):
        shuffle(self.players)
        order = 1
        for player in self.players:
            player.turn_order = order
            order += 1

        self.players.sort()

    def _draw_card(self, player: Player):
        if not player.is_turned:
            item = self.game_pool.pop(0)
            print(f'{player.name} draw a {item}. Items remain:', len(self.game_pool))

            return item

    def turn(self, player: Player):
        item = self._draw_card(player)

        if item:
            if item.type == 'robot':
                player.is_turned = True
                player.turn_no += 1

                if player.current_cell_color:
                    self._remove_cell(player, player.current_cell_color)
                    player.energy_cells -= 1

                    if player.energy_cells == 0:
                        player.current_cell_color = None
                        print(f'Oooops, {player.name} got ROBOT booom. Now he can charge any color.')

                    else:
                        print(f'Oooops, {player.name} got ROBOT booom.')

                elif player.is_protected:
                    print(f'Wow!!! shield saved {player.name} from {item.name}!!!')

                else:
                    print(f'Ahahaha {player.name} died from {item.name}!!! God bye.')
                    self._kill_player(player)

            elif item.type == 'pirate':
                print(f'Oooops, {player.name} got PIRATE booom')
                self.deal_with_pirate(player)
                player.is_turned = True
                player.turn_no += 1

            elif item.type == 'cell':
                player.add_item(item)
                if player.current_cell_color == item.color:
                    player.turn_no += 1
                    print(f'{player.name} got HIS cell color. And draw again...')
                    self.turn(player)
                elif player.turn_no == 2:
                    player.is_turned = True

            elif item.type == 'credit':
                player.add_item(item)
                self._check_credits(player)

                if player.turn_no == 2:
                    player.is_turned = True
                else:
                    player.turn_no += 1
                    self.turn(player)

    def _remove_credits(self, player: Player, count) -> list[Item]:
        draw = []
        for item in player.items:
            if item.type == 'credit':
                draw.append(item)
                player.items.remove(item)
                if len(draw) == count:
                    break

        self._check_credits(player)
        print(f'{player.name} lost {len(draw)} credits. So sad....')
        return draw


    def deal_with_pirate(self, player: Player):
        if player.credits >= 3:
            self.pirate_draw.append(self._remove_credits(player, 3))

        elif player.credits < 3:
            draw = self._remove_credits(player, player.credits)
            if len(draw) < 3:
                pass
            # if len(player.items) >=3:

    @staticmethod
    def _remove_cell(player: Player, color):
        for item in player.items:
            if item.type == 'cell':
                if item.color == color:
                    player.items.remove(item)
                    print(f'{item.name} Removed from {player.name} stash.')
                    break

    def check_charged_colors(self):
        cell_colors = set()
        for player in self.players:
            cell_colors.add(player.current_cell_color)

        return cell_colors

    def _is_free_color(self, color) -> bool:
        free_color = True
        for player in self.players:
            if player.current_cell_color == color:
                free_color = False
                break
            else:
                free_color = True
        return free_color

    def break_shield(self):
        for player in self.players:
            player.is_protected = False

    def charge_cell(self, player: Player, color):

        if self._is_free_color(color):
            if player.current_cell_color:
                if player.current_cell_color == color:
                    player.energy_cells += 1
                    print(f'!!! {player.name} charged one block of '
                          f'{color} color! Now {player.energy_cells}!')
                    self._remove_cell(player, color)
                    self.break_shield()
                    print(f'{player.name} SHIELD DESTROYED!!!! {player.name} charged {color} color')

                    if player.energy_cells == 6:
                        self._is_win(player)
            else:
                player.current_cell_color = color
                player.energy_cells += 1
                self._remove_cell(player, color)
                print(f'!!! First charge for {player.name} charged one block of '
                      f'{color} color! Now {player.energy_cells}!')

                self.break_shield()
                print(f'{player.name} SHIELD DESTROYED!!!! {player.name} charged {color} color')
        else:
            print(f'Sorry {player.name}! You cannot charge {color} color')

    def buy_cell(self, player_seller: Player, player_buyer: Player, item):
        pass

    def _is_win(self, player: Player):
        print(f'WOW, {player.name} CHARGED HIS WARP ENGINE!!!!!!!!! and flew away...')
        self.game_state = 'ended'
        return True

    def _in_stash(self, item: Item, player: Player):
        pass

    @staticmethod
    def _check_credits(player: Player):
        player.credits = 0
        for item in player.items:
            if item.type == 'credit':
                player.credits += 1

        return player.credits

    def _is_dead(self):
        if len(self.players) == 1:
            print(f'{self.players[0].name} is WINNER(alive)! All players are DEAD!')
            self.game_state = 'ended'
            return False
        else:
            return True

    def _kill_player(self, player: Player):
        self.robot_draw.extend(player.items)
        self.players.remove(player)

    def _count_of_items(self, item_type, name=None, index=None):
        count_of = 0
        for item in self.game_pool:
            if item_type == item.type:
                count_of += 1

        return count_of

    @staticmethod
    def _count_of_colors(item_list: list[Item]):
        count_of = {}
        for item in item_list:
            if item.color:
                if item.color in count_of.keys():
                    count_of.update({item.color: int(count_of.get(item.color)) + 1})
                else:
                    count_of.update({item.color: 1})

        return count_of

    # Test function
    def bot_turn(self, player: Player):
        self.turn(player)

        # Found cells
        total_cells = self._count_of_items('cell')
        colors = dict(sorted(self._count_of_colors(player.items).items(), reverse=True, key=itemgetter(1)))

        free_colors = [color for color in colors if self._is_free_color(color)]

        if len(free_colors) >= 1:
            targeted_cell = random.choice(free_colors)
        else:
            targeted_cell = None

        if targeted_cell:
            # if total_cells > 2:
            #     for color in colors:
            #         if colors.get(color) > 1:
            #             # if player.turn_no != 2:
            #             self.charge_cell(player, color)

            # Check turns
            if self.current_turn >= 2:
                if total_cells >= 1:
                    self.charge_cell(player, targeted_cell)

            # Check credits for shopping
            if player.credits == 3:
                pass

    # Test function
    def play_round(self):
        print('\n'.join([str(player) for player in self.players]), '\n')
        for player in self.players:
            player.is_turned = False
            player.turn_no = 1
            if not self.game_state:

                self.bot_turn(player)

                print(player.name, f' ended turn {self.current_turn}')
                if self.current_turn == 3:
                    self.break_shield()

                if not self._is_dead():
                    print('Game ended. All dead.')
                    break

            else:
                print('\n\n'.join([str(player) for player in self.players]))
                exit('Game ended')

        self.current_turn += 1


if __name__ == '__main__':
    players = [Player('Ferhassio', 1),
               Player('Anvoker', 2),
               Player('Denchik', 3),
               Player('Politol', 4)]

    new_game = Game(players)
    for i in range(8):
        print('\n\nRound ', i)
        new_game.play_round()
