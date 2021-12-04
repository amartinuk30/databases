import time
import psycopg2


class Model:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                user="postgres",
                password="qwerty",
                host="localhost",
                port=5432,
                database="lab1",
            )
            self.cursor = self.connection.cursor()
        except:
            print('Error connection...')

    def insert(self, count, query_on_insert, record, type):
        for i in range(int(count)):
            try:
                cursor = self.connection.cursor()
                if type == 'm':
                    cursor.executemany(query_on_insert, record)
                elif type == 'r':
                    cursor.execute(query_on_insert)
                self.connection.commit()
                print(count, "record inserted")
            except (Exception, psycopg2.Error) as error:
                print("{}".format(error))
                self.connection.rollback()
                break
            finally:
                if self.connection:
                    cursor.close()

    def delete(self, records, query_on_delete):
        try:
            cursor = self.connection.cursor()
            cursor.executemany(query_on_delete, records)
            self.connection.commit()
            print(cursor.rowcount, "record deleted")
        except (Exception, psycopg2.Error) as error:
            print("{}".format(error))
            self.connection.rollback()
        finally:
            if self.connection:
                cursor.close()

    def update(self, records, query_on_update):
        try:
            cursor = self.connection.cursor()
            cursor.executemany(query_on_update, records)
            self.connection.commit()
            row_count = cursor.rowcount
            print(row_count, "records updated")
        except (Exception, psycopg2.Error) as error:
            print("{}", error)
            self.connection.rollback()
        finally:
            if self.connection:
                cursor.close()

    def show_table(self, sql_select_query, tab, record, bool):
        try:
            self.cursor = self.connection.cursor()
            if bool:
                beg = int(time.time() * 1000)
            self.cursor.execute(sql_select_query, record)
            if bool:
                end = int(time.time() * 1000) - beg
                print("Time: ", end, " ms")
            records = self.cursor.fetchall()
            return records
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            self.connection.rollback()
        finally:
            if self.connection:
                self.cursor.close()

    def check_id(self, val, num, err_func):
        try:
            rec = [(val,)]
            sql_origin = SqlMiddle.origin_type(num)
            curs = self.connection.cursor()
            curs.execute(sql_origin, rec)
            records = curs.fetchall()
            if records[0] is None:
                for row in records:
                    print("There is row with id: ", row[0])
        except (Exception, psycopg2.Error) as error:
            print("{}".format(error))
            err_func()
        finally:
            if self.connection:
                curs.close()


class SqlMiddle:
    def query_insert_func(num_of_table):
        if num_of_table == '1':
            query_on_insert = """ INSERT INTO player (player_id, player_name, player_salary, agent_id)
            VALUES (%s, %s, %s, %s)"""
        elif num_of_table == '2':
            query_on_insert = """ INSERT INTO contract_offer (offer_id, player_id, club_id, proposed_salary, proposed_duration)
            VALUES (%s, %s, %s, %s, %s)"""
        elif num_of_table == '3':
            query_on_insert = """ INSERT INTO club (club_id, club_name, club_league, coach_id)
            VALUES (%s, %s, %s, %s)"""
        elif num_of_table == '4':
            query_on_insert = """ INSERT INTO head_coach (coach_id, coach_name)
            VALUES (%s, %s)"""
        elif num_of_table == '5':
            query_on_insert = """ INSERT INTO agent (agent_id, agent_name) 
            VALUES (%s, %s)"""
        return query_on_insert

    def query_insert_random_func(num_of_table):
            if num_of_table == '1':
                query_on_random_insert = """ INSERT INTO player (player_id, player_name, player_salary, agent_id)
                SELECT player_id, player_name, player_salary, agent_id FROM
                            (SELECT MAX(player.player_id)+1 as player_id,
                            floor(random()*(200000-80000 + 1) + 80000) as player_salary,
                            substr(md5(random()::text), 0, 15) as player_name,
                            floor(random()*MAX(agent.agent_id))+1 as agent_id 
                            FROM player, agent tablesample BERNOULLI(100)
                            ORDER BY random()) k, generate_series(1, 100000) LIMIT 1
                """
            elif num_of_table == '2':
                query_on_random_insert = """ INSERT INTO contract_offer (offer_id, player_id, club_id, proposed_salary, proposed_duration)
                SELECT offer_id, player_id, club_id, proposed_salary, proposed_duration FROM 
                        (SELECT MAX(contract_offer.offer_id)+1 as offer_id,
                        floor(random()*(200000-80000 + 1) + 80000) as proposed_salary,
                        floor(random()*(5 - 1 + 1) + 1) as proposed_duration,
                        floor(random()*MAX(player.player_id))+1 as player_id,
                        floor(random()*MAX(club.club_id))+1 as club_id 
                        FROM contract_offer, player, club tablesample BERNOULLI(100)
                        ORDER BY random()) k, generate_series(1, 100000) LIMIT 1
                 """
            elif num_of_table == '3':
                query_on_random_insert = """ INSERT INTO club (club_id, club_name, club_league, coach_id)
                            SELECT club_id, club_name, club_league, coach_id FROM
                            (SELECT MAX(club.club_id)+1 as club_id, 
                            substr(md5(random()::text), 0, 15) as club_name,
                            substr(md5(random()::text), 0, 15) as club_league,
                            floor(random()*MAX(head_coach.coach_id))+1 as coach_id 
                            FROM club, head_coach tablesample BERNOULLI(100)
                            ORDER BY random()) k, generate_series(1, 100000) LIMIT 1
                """
            elif num_of_table == '4':
                query_on_random_insert = """ INSERT INTO head_coach (coach_id, coach_name)
                            SELECT coach_id, coach_name FROM
                            (SELECT MAX(head_coach.coach_id)+1 as coach_id,
                            substr(md5(random()::text), 0, 15) as coach_name
                            FROM head_coach tablesample BERNOULLI(100)
                            ORDER BY random()) k ,generate_series(1, 100000) LIMIT 1
                            """
            elif num_of_table == '5':
                query_on_random_insert = """ INSERT INTO agent (agent_id, agent_name)
                SELECT agent_id, agent_name FROM
                            (SELECT MAX(agent.agent_id)+1 as agent_id,
                            substr(md5(random()::text), 0, 15) as agent_name
                            FROM agent tablesample BERNOULLI(100)
                            ORDER BY random()) k ,generate_series(1, 100000) LIMIT 1
                                """
            return query_on_random_insert

    def query_update_func(num_of_table):
        if num_of_table == '1':
            query_on_update = """UPDATE player set player_name = %s, player_salary = %s, agent_id = %s
            WHERE "player_id" = %s """
        elif num_of_table == '2':
            query_on_update = """UPDATE contract_offer set player_id = %s, club_id = %s, proposed_salary = %s, proposed_duration = %s
            WHERE "offer_id" = %s """
        elif num_of_table == '3':
            query_on_update = """UPDATE club set club_name = %s, club_league = %s, coach_id = %s
            WHERE club_id = %s"""
        elif num_of_table == '4':
            query_on_update = """UPDATE head_coach set coach_name = %s
              WHERE coach_id = %s """
        elif num_of_table == '5':
            query_on_update = """UPDATE agent set agent_name = %s
              WHERE agent_id = %s """
        return query_on_update

    def query_delete_func(num_of_table):
        if num_of_table == '1':
            query_on_delete = """ DELETE FROM player WHERE player_id = %s"""
        elif num_of_table == '2':
            query_on_delete = """ DELETE FROM contract_offer WHERE offer_id = %s"""
        elif num_of_table == '3':
            query_on_delete = """ DELETE FROM club WHERE club_id = %s"""
        elif num_of_table == '4':
            query_on_delete = """ DELETE FROM head_coach WHERE coach_id = %s"""
        elif num_of_table == '5':
            query_on_delete = """ DELETE FROM agent WHERE agent_id = %s"""
        return query_on_delete

    def query_specific_func(num_of_table):
        if num_of_table == '1':
            query_on_specific_filter = """select  player_id, player_name, player_salary, agent_name 
            from (select player.player_id, player.player_name, player.player_salary, agent.agent_name
            from player inner join agent on agent.agent_id=player.agent_id  
            where agent.agent_name = %s  group by player.player_id, player.player_name, player.player_salary, agent.agent_name) 
            AS foo where player_id >= %s;
            """
        elif num_of_table == '2':
            query_on_specific_filter = """ select player_name, club_name, proposed_salary, player_salary 
            from (select player_name, club.club_name, player.player_salary, contract_offer.proposed_salary from player inner join contract_offer 
            on player.player_id = contract_offer.player_id inner join club on club.club_id = contract_offer.club_id where club_name = %s 
            group by player.player_name, club.club_name, player.player_salary, contract_offer.proposed_salary) 
            AS foo WHERE player_salary < %s and proposed_salary > %s;
            """
        elif num_of_table == '3':
            query_on_specific_filter = """ select coach_name, club_league, club_name, offer_id, player_id
            from (select coach_name, club_league, club_name, offer_id, player_id from head_coach inner join club
            on club.coach_id = head_coach.coach_id inner join contract_offer on club.club_id = contract_offer.club_id 
            where head_coach.coach_name = %s group by coach_name, club_league, club_name, offer_id, player_id) 
            AS foo WHERE offer_id >= %s and player_id < %s;
            """
        return query_on_specific_filter

    def query_select_func(num_of_table):
        if num_of_table == '1':
            sql_select_query = """ SELECT * FROM player ORDER BY player_id"""
        elif num_of_table == '2':
            sql_select_query = """ SELECT * FROM contract_offer ORDER BY offer_id"""
        elif num_of_table == '3':
            sql_select_query = """ SELECT * FROM club ORDER BY club_id"""
        elif num_of_table == '4':
            sql_select_query = """ SELECT * FROM head_coach ORDER BY coach_id"""
        elif num_of_table == '5':
            sql_select_query = """ SELECT * FROM agent ORDER BY agent_id"""
        return sql_select_query

    def origin_type(num_of_table):
        if num_of_table == 1:
            sql_origin_val = """ SELECT player.player_id FROM player WHERE player_id = %s """
        elif num_of_table == 2:
            sql_origin_val = """ SELECT contract_offer.offer_id FROM contract_offer WHERE offer_id = %s """
        elif num_of_table == 3:
            sql_origin_val = """ SELECT club.club_id FROM club WHERE club_id = %s """
        elif num_of_table == 4:
            sql_origin_val = """ SELECT head_coach.coach_id FROM head_coach WHERE coach_id = %s"""
        elif num_of_table == 5:
            sql_origin_val = """ SELECT agent.agent_id FROM agent WHERE agent_id = %s"""
        return sql_origin_val


def string_validator(value, err_func):
    if value is None or value == '':
        print("ERROR: column cannot contain NULL value")
        err_func()
    return True


def int_validator(value, err_func):
    try:
        int(value)
    except ValueError:
        print("ERROR: WRONG CHARACTER (expected int) !!!")
        err_func()