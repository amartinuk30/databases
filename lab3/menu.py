from enum import Enum
from view import View


class MenuTypes(Enum):
    def __str__(self):
        return str(self.value)

    OPERATIONS = '''
            Main menu :
        1.INSERT TO TABLE
        2.UPDATE DATA
        3.DELETE FROM TABLE
        4.SPECIFIC SELECT
        5.SHOW TABLE
        '''
    TABLES = '''
            Tables :
        1.player
        2.contract_offer
        3.club
        4.head_coach
        5.agent
        '''


class MenuItem(str, Enum):
    INSERT = '1',
    UPDATE = '2',
    DELETE = '3',
    SELECT = '4',
    SHOW = '5'


class Menu:
    def __init__(self, text: str, items: int):
        self.text = text
        self.items = items
        self.choice = self.make_choice()

    def make_choice(self) -> str:
        choice = ""
        valid_items = [str(i) for i in range(1, self.items + 1)]
        while choice not in valid_items:
            choice = View.display(self.text)
        return choice
