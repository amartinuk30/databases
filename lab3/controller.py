from model import Model
from view import View
from menu import Menu, MenuTypes, MenuItem
from userinput import insert_query, update_query, delete_query


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def manage_choice(self):
        table_menu = Menu(MenuTypes.OPERATIONS, 5)
        if table_menu.choice == MenuItem.INSERT:
            table_to_insert = Menu(MenuTypes.TABLES, 5)
            while True:
                record = insert_query(table_to_insert.choice, self.if_exit)
                sql_insert = self.model.query_insert_func(table_to_insert.choice, record[0])
                self.model.insert(sql_insert)
                if self.if_exit() is False:
                    break
            self.if_exit()
        elif table_menu.choice == MenuItem.UPDATE:
            table_to_update = Menu(MenuTypes.TABLES, 5)
            while True:
                record = update_query(table_to_update.choice, self.if_exit, self.model.check_id)
                sql_update = self.model.query_update_func(table_to_update.choice, record[0], self.if_exit)
                self.model.update()
                if self.if_exit() is False:
                    break
            self.if_exit()
        elif table_menu.choice == MenuItem.DELETE:
            table_to_delete = Menu(MenuTypes.TABLES, 5)
            while True:
                record = delete_query(table_to_delete.choice, self.if_exit, self.model.check_id)
                sql_delete = self.model.query_delete_func(table_to_delete.choice, record[0])
                self.model.delete(sql_delete)
                if self.if_exit() is False:
                    break
            self.if_exit()
        elif table_menu.choice == MenuItem.SELECT:
            print("Not supported in this version of the program")
            self.if_exit()
        elif table_menu.choice == MenuItem.SHOW:
            table = Menu(MenuTypes.TABLES, 5)
            sql_select = self.model.query_select_func(table.choice)
            show = self.model.show_table(sql_select)
            self.view.print_table(show, table.choice)
            self.if_exit()

    def if_exit(self):
        ext = View.display("\n\t\t1 --> menu   or    2 --> exit : ")
        if ext == '1':
            self.manage_choice()
        elif ext == '2':
            exit()
        else:
            View.print_text("WRONG CHARACTER !!!")
            self.if_exit()



