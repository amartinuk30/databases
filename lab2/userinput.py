from view import View
from model import string_validator, int_validator


def insert_query(opt, err_func):
    record_to_insert = ""
    if opt == '1':
        player_id = View.display("player_id: ")
        int_validator(player_id, err_func)

        player_name = View.display("player_name: ")
        string_validator(player_name, err_func)

        player_salary = View.display("player_salary: ")
        int_validator(player_salary, err_func)

        agent_id = View.display("agent_id: ")

        if agent_id:
            int_validator(agent_id, err_func)
            record_to_insert = [(player_id, player_name, player_salary, agent_id)]
        else:
            record_to_insert = [(player_id, player_name, player_salary, None)]
    elif opt == '2':
        offer_id = View.display("offer_id: ")
        int_validator(offer_id, err_func)

        player_id = View.display("player_id: ")
        int_validator(player_id, err_func)

        club_id = View.display("club_id: ")
        int_validator(club_id, err_func)

        proposed_salary = View.display("proposed_salary: ")
        int_validator(proposed_salary, err_func)

        proposed_duration = View.display("proposed_duration: ")
        int_validator(proposed_duration, err_func)

        record_to_insert = [(offer_id, player_id, club_id, proposed_salary, proposed_duration)]
    elif opt == '3':
        club_id = View.display("club_id: ")
        int_validator(club_id, err_func)

        club_name = View.display("club_name: ")
        string_validator(club_name, err_func)

        club_league = View.display("club_league: ")
        string_validator(club_league, err_func)

        coach_id = View.display("coach_id: ")
        int_validator(coach_id, err_func)

        record_to_insert = [(club_id, club_name, club_league, coach_id)]
    elif opt == '4':
        coach_id = View.display("coach_id: ")
        int_validator(coach_id, err_func)

        coach_name = View.display("coach_name: ")
        string_validator(coach_name, err_func)

        record_to_insert = [(coach_id, coach_name)]
    elif opt == '5':
        agent_id = View.display("agent_id: ")
        int_validator(agent_id, err_func)

        agent_name = View.display("agent_name: ")
        string_validator(agent_name, err_func)

        record_to_insert = [(agent_id, agent_name)]
    return record_to_insert

def update_query(opt, err_func, is_valid_func) -> str:
    record_to_update = ""
    if opt == '1':
        player_id = View.display("Edit line where player_id = :")
        string_validator(player_id, err_func)

        player_name = View.display("player_name: ")
        string_validator(player_name, err_func)

        player_salary = View.display("player_salary: ")
        string_validator(player_salary, err_func)

        agent_id = View.display("agent_id: ")
        string_validator(agent_id, err_func)

        record_to_update = [(player_name, player_salary, agent_id, player_id)]
    elif opt == '2':
        offer_id = View.display("Edit line where offer_id = :")
        int_validator(offer_id, err_func)

        player_id = View.display("player_id: ")
        string_validator(player_id, err_func)

        club_id = View.display("club_id: ")
        string_validator(club_id, err_func)

        proposed_salary = View.display("proposed_salary: ")
        int_validator(proposed_salary, err_func)

        proposed_duration = View.display("proposed_duration :")
        int_validator(proposed_duration, err_func)

        is_valid_func(offer_id, 2, err_func)
        record_to_update = [(player_id, club_id, proposed_salary, proposed_duration, offer_id)]
    elif opt == '3':
        club_id = View.display("Edit line where club_id = :")
        int_validator(club_id, err_func)

        club_name = View.display("club_name: ")
        string_validator(club_name, err_func)

        club_league = View.display("club_league: ")
        string_validator(club_league, err_func)

        coach_id = View.display("coach_id :")
        int_validator(coach_id, err_func)

        is_valid_func(club_id, 3, err_func)
        record_to_update = [(club_name, club_league, coach_id, club_id)]
    elif opt == '4':
        coach_id = View.display("Edit line where coach_id = :")
        int_validator(coach_id, err_func)

        coach_name = View.display("coach_name: ")
        string_validator(coach_name, err_func)

        is_valid_func(coach_id, 4, err_func)
        record_to_update = [(coach_name, coach_id)]
    elif opt == '5':
        agent_id = View.display("Edit line where agent_id = :")
        int_validator(agent_id, err_func)

        agent_name = View.display("agent_name: ")
        string_validator(agent_name, err_func)

        is_valid_func(agent_id, 5, err_func)
        record_to_update = [(agent_name, agent_id)]
    return record_to_update


def delete_query(opt, err_func, is_valid_func):
    record_to_delete = ""
    if opt == '1':
        player_id = View.display("Delete line for this player_id:")
        int_validator(player_id, err_func)
        is_valid_func(player_id, 1, err_func)
        record_to_delete = [(player_id,)]
    elif opt == '2':
        offer_id = View.display("Delete line for this offer_id: ")
        int_validator(offer_id, err_func)
        is_valid_func(offer_id, 2, err_func)
        record_to_delete = [(offer_id,)]
    elif opt == '3':
        club_id = View.display("Delete line for this club_id: ")
        int_validator(club_id, err_func)
        is_valid_func(club_id, 3, err_func)
        record_to_delete = [(club_id,)]
    elif opt == '4':
        coach_id = View.display("Delete line for this coach_id: ")
        int_validator(coach_id, err_func)
        is_valid_func(coach_id, 4, err_func)
        record_to_delete = [(coach_id,)]
    elif opt == '5':
        agent_id = View.display("Delete line for this agent_id: ")
        int_validator(agent_id, err_func)
        is_valid_func(agent_id, 5, err_func)
        record_to_delete = [(agent_id,)]
    return record_to_delete


def spec_choose():
    table = 0
    print("""1) Show 'player_id', 'player_name', 'player_salary', 'agent_name', 
                where 'agent_name' = ... and 'player_id' >= ...
                  """)
    print("""2) Show 'player_name', 'club_name', 'proposed_salary', 'player_salary',
                where 'club_name' = ... and 'player_salary' < ... and 'proposed_salary' > ...
                  """)
    print("""3) Show 'coach_name', 'club_league', 'club_name', 'offer_id', 'player_id',
                where 'coach_name' = ... and 'offer_id' >= ... and 'player_id' < ...
                  """)
    while table != '1' and table != '2' and table != '3':
        table = input("\n\t\tYour choice : ")
    return table

def specific_query(opt, err_func):
    if opt == '1':
        player_id = View.display("player_id >= : ")
        int_validator(player_id, err_func)

        agent_name = View.display("agent_name = : ")
        string_validator(agent_name, err_func)

        record_to_specific = (agent_name, player_id)
    elif opt == '2':
        club_name = View.display("club_name = : ")
        string_validator(club_name, err_func)

        player_salary = View.display("player_salary < : ")
        int_validator(player_salary, err_func)

        proposed_salary = View.display("proposed_salary > : ")
        int_validator(proposed_salary, err_func)

        record_to_specific = (club_name, player_salary, proposed_salary)
    elif opt == '3':
        coach_name = View.display("coach_name = : ")
        string_validator(coach_name, err_func)

        offer_id = View.display("offer_id >= : ")
        int_validator(offer_id, err_func)

        player_id = View.display("player_id < : ")
        int_validator(player_id, err_func)

        record_to_specific = (coach_name, offer_id, player_id)
    return record_to_specific





