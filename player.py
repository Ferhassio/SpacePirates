from components import Item


class Player:
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.energy_cells = 0
        self.current_cell_color = None
        self.credits = 0
        self.items = []
        self.is_protected = True
        self.is_turned = False
        self.turn_no = 1
        self.turn_order = None

    def add_item(self, item: Item):
        self.items.append(item)

    def __str__(self):
        items = ' | '.join([str(item) for item in self.items])

        return f'[{self.index}]({self.turn_order}) {self.name} ' \
               f'(color:{self.current_cell_color}, cells: {self.energy_cells}, ' \
               f'credits: {self.credits}) Items: ' + items

    def __repr__(self):
        return f'[#{self.index}] {self.name}'

    def __lt__(self, other):
        return self.turn_order < other.turn_order
