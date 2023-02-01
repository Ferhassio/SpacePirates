import random


class Item:
    def __init__(self, name, price, item_type, color, item_id, desc=None):
        self.description = desc
        self.type = item_type
        self.color = color if color else None
        self.price = price
        self.item_id = item_id
        self.pic = ''
        self.name = name + f' ({self.color})' if item_type == 'cell' else name

    def __str__(self):
        return f'[{str(self.item_id)}] {self.name}'

    def __lt__(self, other):
        return self.price < other.price


class ItemPoolMaster:
    def __init__(self, players, item_map: list):
        """
        Item generator class for game.
        Example: [('credit', 10), ('pirate', 5)]
        :param item_map: tuple (item_type, count)
        """
        self.players = players
        self.requested_pool = item_map
        self.TYPE_LIST = {'credit': 'Кристалл', 'cell': 'Энергоячейка', 'pirate': 'Пират', 'robot': 'Робот'}
        self.COLORS = ['red', 'green', 'blue', 'black', 'white', 'yellow', 'pink', 'orange', 'teal', 'magenta']
        self.root_index = 0
        random.shuffle(self.COLORS)

        self.pool = []

        # self._generate_cells()

    def _generate_cells(self):
        colored_cells = []
        cell_price = 3
        cell_count = 6

        for player in range(1, self.players + 1):
            colored_cells.extend([Item(self.TYPE_LIST.get('cell'), cell_price, 'cell', self.COLORS[player], idx)
                                  for idx in range(1, cell_count + 1)])

        random.shuffle(colored_cells)
        self.root_index += len(colored_cells)

        return colored_cells

    def _generate_items(self):
        item_price = 0
        item_pool = []
        for item_tuple in self.requested_pool:
            item_type, count = item_tuple
            if item_type not in self.TYPE_LIST.keys():
                print(f'Type {item_type} does not exist. Choose from: {list(self.TYPE_LIST.keys())}')
                break

            item_pool.extend([Item(self.TYPE_LIST.get(item_type), item_price, item_type, None, self.root_index + idx)
                              for idx in range(1, count + 1)])
        random.shuffle(item_pool)

        return item_pool

    def build_pool(self):
        full_item_pool = self._generate_cells() + self._generate_items()
        random.shuffle(full_item_pool)

        self.pool = full_item_pool

        return self.pool

    def shuffle(self):
        random.shuffle(self.pool)


if __name__ == '__main__':
    pool_generator = ItemPoolMaster(5, [('credit', 50), ('robot', 8), ('pirate', 15)])
    items = pool_generator.build_pool()
    print('\n'.join([str(i) for i in items]))
    print('Game started. Total items:', len(items))
    items[1].item_id = 10000
    print('\n'.join([str(i) for i in items]))

    # credits = 0
    # killed = 0
    # player_items = []
    #
    # for item in item_pool:
    #     if item.type == 'credit':
    #         credits += 1
    #         player_items.append(item)
    #     elif item.type == 'pirate':
    #         for it in player_items:
    #             if it.type == 'credit':
    #                 if player_items.count(it.type) == 3:
    #                     _ = [player_items.remove(it) for _ in range(4)]
    #                     credits -= 3
    #                 if player_items.count(it.type) < 3:
    #                     _ = [player_items.remove(it) for _ in range(player_items.count(it.type)+1)]
    #                     credits -= player_items.count(it.type)
    #     elif item.type == 'robot':
    #
    #
    # print('Credits', credits)


