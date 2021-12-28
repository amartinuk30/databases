from prettytable import PrettyTable


class View:
    def print_table(self, records, tab):
        table = PrettyTable()
        if tab == '1':
            table.field_names = ["player_id", "player_name", "player_salary", "agent_id"]
            for sql_row in records:
                table.add_row([sql_row.player_id, sql_row.player_name, sql_row.player_salary, sql_row.agent_id])
            print(table)
        elif tab == '2':
            table.field_names = ["offer_id", "player_id", "club_id", "proposed_salary", "proposed_duration"]
            for sql_row in records:
                table.add_row([sql_row.offer_id, sql_row.player_id, sql_row.club_id, sql_row.proposed_salary, sql_row.proposed_duration])
            print(table)
        elif tab == '3':
            table.field_names = ["club_id", "club_name", "club_league", "coach_id"]
            for sql_row in records:
                table.add_row([sql_row.club_id, sql_row.club_name, sql_row.club_league, sql_row.coach_id])
            print(table)
        elif tab == '4':
            table.field_names = ["coach_id", "coach_name"]
            for sql_row in records:
                table.add_row([sql_row.coach_id, sql_row.coach_name])
            print(table)
        elif tab == '5':
            table.field_names = ["agent_id", "agent_name"]
            if records:
                for sql_row in records:
                    table.add_row([sql_row.agent_id, sql_row.agent_id])
                print(table)
        elif tab == '6':
            table.field_names = ["player_id", "player_name", "player_salary", "agent_name"]
            if records:
                for sql_row in records:
                    table.add_row([sql_row.player_id, sql_row.player_name, sql_row.player_salary, sql_row.agent_name])
                print(table)
            else:
                print("Not found")
        elif tab == '7':
            table.field_names = ["player_name", "club_name", "player_salary", "proposed_salary"]
            if records:
                for sql_row in records:
                    table.add_row([sql_row.player_name, sql_row.club_name, sql_row.player_salary, sql_row.proposed_salary])
                print(table)
            else:
                print("Not found")
        elif tab == '8':
            table.field_names = ["coach_name", "club_league", "club_name", "offer_id", "player_id"]
            if records:
                for sql_row in records:
                    table.add_row([sql_row.coach_name, sql_row.club_league, sql_row.club_name, sql_row.offer_id, sql_row.player_id])
                print(table)
            else:
                print("Not found")

    @staticmethod
    def display(txt):
        return input(txt)

    @staticmethod
    def print_text(txt):
        print(str(txt))
