import random
from operator import itemgetter

from components import Item, ItemPoolMaster
from player import Player
from random import shuffle


class Game:
    def __init__(self, players_list: list[Player]):
        self.default_items = [('credit', 50), ('robot', 10), ('pirate', 20)]

        self.ItemPoolGenerator = ItemPoolMaster(len(players_list), self.default_items)
        self.game_pool = self.ItemPoolGenerator.build_pool()

        self.players = players_list
        self.total_players = len(players_list)
        self.current_turn = 0

        self.pirate_draw = []
        self.robot_draw = []
        self.colors_in_game = {}

        self.pirate_meet = 0
        self.robot_meet = 0

        self.game_state = None

        self.set_order()
        print('Game data loaded. Total items:', len(self.game_pool))

    def _check_robot_draw(self):
        if self.robot_meet == self.total_players:
            self.robot_meet = 0
            self.game_pool.extend(self.robot_draw)
            self.robot_draw.clear()
            print(f'WOW players meet {self.total_players} ROBOTS! '
                  f'Pool shuffled. New len: {len(self.game_pool)}')
            random.shuffle(self.game_pool)

    def _check_pirate_draw(self):
        if self.pirate_meet == self.total_players + 4:
            self.pirate_meet = 0
            self.game_pool.extend(self.pirate_draw)
            self.pirate_draw.clear()
            print(f'WOW players deal with {self.total_players + 4} PIRATES! '
                  f'Pool shuffled. New len: {len(self.game_pool)}')

            random.shuffle(self.game_pool)

    def set_order(self) -> None:
        """
        Set turn order for players
        :return: None
        """
        shuffle(self.players)
        order = 1
        for player in self.players:
            player.turn_order = order
            order += 1

        self.players.sort()

    def _draw_card(self, player: Player) -> Item:
        """
        Draw an item from pool
        :param player: Player object
        :return: Item object
        """
        if not player.is_turned:
            item = self.game_pool.pop(0)
            print(f'{player.name} draw a {item}. Items remain:', len(self.game_pool))

            return item

    @staticmethod
    def _consume_cell(player: Player, cell_color) -> Item:
        """
        Use cell for charging engine. Change its property to `placed`
        :param player: Player object
        :param cell_color: Desired cell
        :return: Item object
        """
        cell = None
        for item in player.items:
            if item.type == 'cell':
                # print('ITEM:', item.name)
                if item.color == cell_color:
                    if not item.placed:
                        print(f'{item.name} used by {player.name}.')
                        item.placed = True
                        cell = item

        return cell

    @staticmethod
    def _remove_cell(player: Player, cell_color) -> Item:
        """
        TODO: Remove this or concat with `_consume_cell`
        """
        cell = None
        for item in player.items:
            if item.type == 'cell':
                # print('ITEM:', item.name)
                if item.color == cell_color:
                    print(f'{item.name} REMOVED from {player.name} stash.')
                    item.placed = True
                    cell = item
                    break

        return cell

    def turn(self, player: Player) -> None:
        """
        Make a full turn
        :param player: Player object
        :return: None
        """

        # Draw a card
        item = self._draw_card(player)
        if item:
            # check various item types
            if item.type == 'robot':

                # Add robot item in draw
                self.robot_draw.append(item)
                player.is_turned = True
                player.turn_no += 1

                # If player has a placed color
                if player.current_cell_color:
                    player.energy_cells -= 1

                    # Remove cell and add to robot draw
                    removed_cell = self._remove_cell(player, player.current_cell_color)
                    self.robot_draw.append(removed_cell)

                    # Drop player color if run out of cells
                    if player.energy_cells == 0:
                        player.current_cell_color = None
                        print(f'Oooops, {player.name} got ROBOT booom. Now he can charge any color. '
                              f'Draw {len(self.robot_draw)}')
                        # print(' '.join([str(itm) for itm in self.robot_draw]))

                    else:
                        print(f'Oooops, {player.name} got ROBOT booom. '
                              f'Draw {len(self.robot_draw)}')
                        # print(' '.join([str(itm) for itm in self.robot_draw]))

                # 3 turn protection
                elif player.is_protected:
                    print(f'Wow!!! shield saved {player.name} from {item.name}!!!')
                else:
                    print(f'Ahahaha {player.name} died from {item.name}!!! God bye. Draw {len(self.robot_draw)}')
                    # print(' '.join([str(itm) for itm in self.robot_draw]))

                    # Wipe player
                    self._kill_player(player)

                self.robot_meet += 1
                self._check_robot_draw()

            elif item.type == 'pirate':
                print(f'Oooops, {player.name} got PIRATE booom. Draw {len(self.pirate_draw)}')
                self.pirate_draw.append(item)
                self.deal_with_pirate(player)

                player.is_turned = True
                player.turn_no += 1

                self.pirate_meet += 1
                self._check_pirate_draw()

            elif item.type == 'cell':
                # add cell to player inventory
                player.add_item(item)

                # If cell is player color, turn again
                if player.current_cell_color == item.color:
                    player.turn_no += 1
                    print(f'{player.name} got HIS cell color. And draw again...')
                    self.turn(player)
                elif player.turn_no == 2:
                    player.is_turned = True

            elif item.type == 'credit':
                player.add_item(item)

                # check balance for all players
                self._check_credits(player)

                if player.turn_no == 2:
                    player.is_turned = True
                else:
                    player.turn_no += 1
                    self.turn(player)

    def _remove_credits(self, player: Player, count) -> list[Item]:
        """
        Remove `credit` item type from player inventory
        :param player: Player object
        :param count: count of credits to remove
        :return: list of removed credits
        """
        draw = []
        for item in player.items:
            # Search all credits until limit
            if item.type == 'credit':
                draw.append(item)
                player.items.remove(item)
                if len(draw) == count:
                    break

        self._check_credits(player)
        print(f'{player.name} lost {len(draw)} credits. So sad....')
        return draw

    def deal_with_pirate(self, player: Player):
        # TODO: Add some logic
        if player.credits >= 3:
            self.pirate_draw.extend(self._remove_credits(player, 3))

        elif player.credits < 3:
            draw = self._remove_credits(player, player.credits)
            if len(draw) < 3:
                pass
            # if len(player.items) >=3:

    def _reset_item_state(self) -> None:
        """
        Reset Item `placed` state to normal
        :return: None
        """

        # check robot draw
        for item in self.robot_draw:
            item.placed = False

        # check pirate draw
        for item in self.pirate_draw:
            item.placed = False

    def _is_free_color(self, color) -> bool:
        """
        Bot logic to detect possible turn
        :param color: Desired color to try
        :return: True if possible else False
        """
        free_color = True
        for player in self.players:
            # If we found player with desired we need to break,
            # cuz only one color in game
            if player.current_cell_color == color:
                free_color = False
                break
            else:
                free_color = True

        return free_color

    def break_shield(self) -> None:
        """
        Destroy starter protection if player charge smth or after 3 rounds
        :return: None
        """
        for player in self.players:
            player.is_protected = False

    def charge_cell(self, player: Player, color):
        """
        Charge cell from inventory.
        :param player: Player object
        :param color: desired color to charge
        :return: None
        """

        # Check if possible to charge and possibility for player to use this cell
        if self._is_free_color(color):
            if player.current_cell_color:
                if player.current_cell_color == color:
                    player.energy_cells += 1
                    print(f'!!! {player.name} charged one block of '
                          f'{color} color! Now {player.energy_cells}!')
                    self._consume_cell(player, color)
                    self.break_shield()
                    print(f'{player.name} SHIELD DESTROYED!!!! {player.name} charged {color} color.')

                    if player.energy_cells == 6:
                        self._is_win(player)

            # If player got first cell
            else:
                player.current_cell_color = color
                player.energy_cells += 1
                self._consume_cell(player, color)
                print(f'!!! First charge for {player.name} charged of '
                      f'{color} color! Now {player.energy_cells}!')

                self.break_shield()
                print(f'{player.name} SHIELD DESTROYED!!!! {player.name} charged {color} color')
        else:
            print(f'Sorry {player.name}! You cannot charge {color} color')

    def buy_cell(self, player_seller: Player, player_buyer: Player, item):
        pass

    def _is_win(self, player: Player) -> bool:
        """
        Event trigger for `Engine WIN`
        :param player: Player object
        :return: True
        """
        print(f'WOW, {player.name} CHARGED HIS WARP ENGINE!!!!!!!!! and flew away...')
        self.game_state = 'ended'
        return True

    @staticmethod
    def _check_credits(player: Player) -> int:
        """
        Check how many credits player have
        :param player: Player object
        :return: number of credits
        """
        # Drop credits for recalculating
        player.credits = 0
        for item in player.items:
            if item.type == 'credit':
                player.credits += 1

        return player.credits

    def _is_dead(self) -> bool:
        """
        Trigger for `LastManStand WIN`
        :return: True if winner else False
        """

        if len(self.players) == 1:
            print(f'{self.players[0].name} is WINNER(alive)! All players are DEAD!')
            self.game_state = 'ended'
            return False
        else:
            return True

    def _kill_player(self, player: Player) -> None:
        """
        Remove player from active player list
        :param player: Player object
        :return: None
        """
        self.robot_draw.extend(player.items)
        self.players.remove(player)

    def _count_of_items(self, item_type, name=None, index=None):
        """
        Calculate items in pool
        :param item_type: item type
        :param name: UnderConstruction
        :param index: UnderConstruction
        :return: count of items
        """
        count_of = 0
        for item in self.game_pool:
            if item_type == item.type:
                count_of += 1

        return count_of

    @staticmethod
    def _count_of_colors(item_list: list[Item]):
        """
        Calculate count of colors in Item list
        :param item_list: list of `Item` object
        :return: count of items
        """
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
        print('\n\n'.join([str(player) for player in self.players]), '\n')
        self._reset_item_state()

        print('Robot draw', len(self.robot_draw))
        print('Pirate draw', len(self.pirate_draw))

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
                # print('\n\n'.join([str(player) for player in self.players]))
                exit('Game ended')

        self.current_turn += 1


if __name__ == '__main__':
    players = [Player('Ferhassio', 1),
               Player('Anvoker', 2),
               Player('Denchik', 3),
               Player('Politol', 4)]

    new_game = Game(players)
    for i in range(1000):
        print('\n\nRound ', i)
        new_game.play_round()
