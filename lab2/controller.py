from model import Model, SqlMiddle, int_validator
from view import View
from menu import Menu, MenuTypes, MenuItem
from userinput import insert_query, update_query, delete_query, spec_choose, specific_query


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def manage_choice(self):
        table_menu = Menu(MenuTypes.OPERATIONS, 5)

        if table_menu.choice == MenuItem.INSERT:
            table_to_insert = Menu(MenuTypes.TABLES, 5)
            if_rand = self.type_of_insert()
            if if_rand == '1':
                while True:
                    sql_insert = SqlMiddle.query_insert_func(table_to_insert.choice)
                    record = insert_query(table_to_insert.choice, self.if_exit)
                    self.model.insert('1', sql_insert, record, 'm')
                    if self.if_exit() is False:
                        break
            elif if_rand == '2':
                pass
                times = View.display("The number of lines you want to generate:")
                int_validator(times, self.if_exit)
                sql_random = SqlMiddle.query_insert_random_func(table_to_insert.choice)
                self.model.insert(times, sql_random, None, 'r')
                self.if_exit()
        elif table_menu.choice == MenuItem.UPDATE:
            table_to_update = Menu(MenuTypes.TABLES, 5)
            while True:
                sql_update = SqlMiddle.query_update_func(table_to_update.choice)
                record = update_query(table_to_update.choice, self.if_exit, self.model.check_id)
                self.model.update(record, sql_update)
                if self.if_exit() is False:
                    break
            self.if_exit()
        elif table_menu.choice == MenuItem.DELETE:
            table_to_delete = Menu(MenuTypes.TABLES, 5)
            while True:
                sql_delete = SqlMiddle.query_delete_func(table_to_delete.choice)
                record = delete_query(table_to_delete.choice, self.if_exit, self.model.check_id)
                self.model.delete(record, sql_delete)
                if self.if_exit() is False:
                    break
            self.if_exit()
        elif table_menu.choice == MenuItem.SELECT:
            table = spec_choose()
            tab = str(int(table)+5)
            to_record = specific_query(table, self.if_exit)
            sql_spec = SqlMiddle.query_specific_func(table)
            show = self.model.show_table(sql_spec, tab, to_record, True)
            self.view.print_table(show, tab)
            self.if_exit()
        elif table_menu.choice == MenuItem.SHOW:
            table = Menu(MenuTypes.TABLES, 5)
            sql_select = SqlMiddle.query_select_func(table.choice)
            show = self.model.show_table(sql_select, table.choice, None, False)
            self.view.print_table(show, table.choice)
            self.if_exit()

    def type_of_insert(self):
        option = View.display("\n\t\t1 --> manual insertion   or  2 --> random insertion : ")
        if option != '1' and option != '2':
            View.print_text("WRONG CHARACTER !!!")
            self.if_exit()
        return option

    def if_exit(self):
        ext = View.display("\n\t\t1 --> menu   or    2 --> exit : ")
        if ext == '1':
            self.manage_choice()
        elif ext == '2':
            exit()
        else:
            View.print_text("WRONG CHARACTER !!!")
            self.if_exit()



