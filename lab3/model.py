from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey


class Model:
    #connection to PostgreSQL server
    Base = declarative_base()

    def __init__(self):
        try:
            self.engine = create_engine('postgresql+psycopg2://postgres:qwerty@localhost/lab1')
            self.Session = sessionmaker(bind=self.engine)
            self.s = self.Session()
        except exc.SQLAlchemyError as e:
            print(type(e))

    def insert(self, sql_insert_query):
        try:
            self.s.add(sql_insert_query)
            self.s.commit()
            print("Successfully inserted")
        except exc.SQLAlchemyError as error :
            print("Failed inserting record into table {}".format(error))
            self.s.rollback()

    def delete(self, sql_delete_query):
        try:
            self.s.delete(sql_delete_query)
            self.s.commit()
            print("Successfully deleted")
        except exc.SQLAlchemyError as error:
            print("Failed deleting record into table {}".format(error))
            self.s.rollback()

    # update table row
    def update(self):
        try:
            self.s.commit()
            print("Successfully updated")
        except exc.SQLAlchemyError as error:
            print("Failed updating record of the table {}", error)
            self.s.rollback()

    def show_table(self, sql_select_query):
        try:
            records = sql_select_query.all()
        except exc.SQLAlchemyError as error:
            print("Error while fetching data from PostgreSQL", error)
            self.s.rollback()
        return records

    def check_id(self, val, num, if_exit):
        try:
            sql_origin = self.origin_type(num, val)
            if sql_origin is None:
                raise exc.SQLAlchemyError
        except exc.SQLAlchemyError as error:
            print("Failed, there are no records with such id")
            if_exit()

    def query_insert_func(self, num_of_table, record):
        if num_of_table == '1':
            query_on_insert = Player(record[0], record[1], record[2], record[3])
        elif num_of_table == '2':
            query_on_insert = Contract_offer(record[0], record[1], record[2], record[3], record[4])
        elif num_of_table == '3':
            query_on_insert = Club(record[0], record[1], record[2], record[3])
        elif num_of_table == '4':
            query_on_insert = Head_coach(record[0], record[1])
        elif num_of_table == '5':
            query_on_insert = Agent(record[0], record[1])
        return query_on_insert

    def query_update_func(self, num_of_table, val, if_exit):
        try:
            if num_of_table == '1':
                #query_on_update = """UPDATE player set player_name = %s, player_salary = %s, agent_id = %s
                #WHERE "player_id" = %s """
                query_on_update = self.s.query(Player).filter(Player.player_id == val[0]). \
                    update({Player.player_name: val[1], Player.player_salary: val[2], Player.agent_id: val[3]})
            elif num_of_table == '2':
                #query_on_update = """UPDATE contract_offer set player_id = %s, club_id = %s, proposed_salary = %s, proposed_duration = %s
                #WHERE "offer_id" = %s """
                query_on_update = self.s.query(Contract_offer).filter(Contract_offer.offer_id == val[0]). \
                    update({Contract_offer.player_id: val[1], Contract_offer.club_id: val[2], Contract_offer.proposed_salary: val[3], Contract_offer.proposed_duration: val[4]})
            elif num_of_table == '3':
               #query_on_update = """UPDATE club set club_name = %s, club_league = %s, coach_id = %s
                #WHERE club_id = %s"""
               query_on_update = self.s.query(Club).filter(Club.club_id == val[0]). \
                   update({Club.club_name: val[1], Club.club_league: val[2], Club.coach_id: val[3]})
            elif num_of_table == '4':
                #query_on_update = """UPDATE head_coach set coach_name = %s
                #  WHERE coach_id = %s """
                query_on_update = self.s.query(Head_coach).filter(Head_coach.coach_id == val[0]). \
                    update({Head_coach.coach_id: val[1]})
            elif num_of_table == '5':
                #query_on_update = """UPDATE agent set agent_name = %s
                #WHERE agent_id = %s """
                query_on_update = self.s.query(Agent).filter(Agent.agent_id == val[0]). \
                    update({Agent.agent_name: val[1]})
        except exc.SQLAlchemyError as error:
            print("Failed updating record of the table {}", error)
            if_exit()
        return query_on_update

    def query_delete_func(self, num_of_table, rec):
        try:
            if num_of_table == '1':
                query_on_delete = self.s.query(Player).filter_by(player_id=rec[0]).one()
            elif num_of_table == '2':
                query_on_delete = self.s.query(Contract_offer).filter_by(offer_id=rec[0]).one()
            elif num_of_table == '3':
                query_on_delete = self.s.query(Club).filter_by(club_id=rec[0]).one()
            elif num_of_table == '4':
                query_on_delete = self.s.query(Head_coach).filter_by(coach_id=rec[0]).one()
            elif num_of_table == '5':
                query_on_delete = self.s.query(Agent).filter_by(agent_id=rec[0]).one()
        except exc.SQLAlchemyError as error:
            print("Failed deleting record from table {}".format(error))
        finally:
            return query_on_delete

    def query_select_func(self, num_of_table):
        if num_of_table == '1':
            #sql_select_query = """ SELECT * FROM player ORDER BY player_id"""
            sql_select_query = self.s.query(Player).order_by(Player.player_id)
        elif num_of_table == '2':
            #sql_select_query = """ SELECT * FROM contract_offer ORDER BY offer_id"""
            sql_select_query = self.s.query(Contract_offer).order_by(Contract_offer.offer_id)
        elif num_of_table == '3':
            #sql_select_query = """ SELECT * FROM club ORDER BY club_id"""
            sql_select_query = self.s.query(Club).order_by(Club.club_id)
        elif num_of_table == '4':
            #sql_select_query = """ SELECT * FROM head_coach ORDER BY coach_id"""
            sql_select_query = self.s.query(Head_coach).order_by(Head_coach.coach_id)
        elif num_of_table == '5':
            #sql_select_query = """ SELECT * FROM agent ORDER BY agent_id"""
            sql_select_query = self.s.query(Agent).order_by(Agent.agent_id)
        return sql_select_query

    def origin_type(self, num_of_table, val):
        if num_of_table == 1:
            #sql_origin_val = """ SELECT player.player_id FROM player WHERE player_id = %s """
            sql_origin_val = self.s.query(Player).filter_by(player_id=val).one_or_none()
        elif num_of_table == 2:
            #sql_origin_val = """ SELECT contract_offer.offer_id FROM contract_offer WHERE offer_id = %s """
            sql_origin_val = self.s.query(Contract_offer).filter_by(offer_id=val).one_or_none()
        elif num_of_table == 3:
            #sql_origin_val = """ SELECT club.club_id FROM club WHERE club_id = %s """
            sql_origin_val = self.s.query(Club).filter_by(club_id=val).one_or_none()
        elif num_of_table == 4:
            #sql_origin_val = """ SELECT head_coach.coach_id FROM head_coach WHERE coach_id = %s"""
            sql_origin_val = self.s.query(Head_coach).filter_by(coach_id=val).one_or_none()
        elif num_of_table == 5:
            #sql_origin_val = """ SELECT agent.agent_id FROM agent WHERE agent_id = %s"""
            sql_origin_val = self.s.query(Agent).filter_by(agent_id=val).one_or_none()
        return sql_origin_val

class Contract_offer(Model.Base):
    __tablename__ = 'contract_offer'
    offer_id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('player.player_id'))
    club_id = Column(Integer, ForeignKey('club.club_id'))
    proposed_salary = Column(Integer)
    proposed_duration = Column(Integer)

    club_r = relationship("Club", back_populates="player_s")
    player_r = relationship("Player", back_populates="club_s")

    def __init__(self, offer_id, player_id, club_id, proposed_salary, proposed_duration):
        self.offer_id = offer_id
        self.player_id = player_id
        self.club_id = club_id
        self.proposed_salary = proposed_salary
        self.proposed_duration = proposed_duration


class Club(Model.Base):
    __tablename__ = 'club'
    club_id = Column(Integer, primary_key=True)
    club_name = Column(String(32))
    club_league = Column(String(32))
    coach_id = Column(Integer, ForeignKey('head_coach.coach_id'))
    player_s = relationship("Contract_offer", back_populates="club_r")

    def __init__(self, club_id, club_name, club_league, coach_id):
        self.club_id = club_id
        self.club_name = club_name
        self.club_league = club_league
        self.coach_id = coach_id


class Head_coach(Model.Base):
    __tablename__ = 'head_coach'
    coach_id = Column(Integer, primary_key=True)
    coach_name = Column(String(32))

    def __init__(self, coach_id, coach_name):
        self.coach_id = coach_id
        self.coach_name = coach_name


class Player(Model.Base):
    __tablename__ = 'player'
    player_id = Column(Integer, primary_key=True)
    player_name = Column(String(32))
    player_salary = Column(Integer)
    agent_id = Column(Integer, ForeignKey('agent.agent_id'))

    club_s = relationship("Contract_offer", back_populates="player_r")
    agent = relationship("Agent")

    def __init__(self, player_id, player_name, player_salary, agent_id):
        self.player_id = player_id
        self.player_name = player_name
        self.player_salary = player_salary
        self.agent_id = agent_id


class Agent(Model.Base):
    __tablename__ = 'agent'
    agent_id = Column(Integer, primary_key=True)
    agent_name = Column(String(32))

    def __init__(self, agent_id, agent_name):
        self.agent_id = agent_id
        self.agent_name = agent_name


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