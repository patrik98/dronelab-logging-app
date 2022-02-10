import sqlalchemy as db
from sqlalchemy.orm import Session
import pandas as pd
from pandas.core.frame import DataFrame
from .model import Position

class Database:
    """
    Class to handle database connection and operations
    """
    def __init__(self, config, insert_limit=16):
        """
        @param config: Dictionary
        @param insert_limit: Integer
        @return: Database

        Example config:
        {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'user',
            'password': 'pw',
            'database': 'db'
        }
        """
        self.engine = self.__get_engine(config)
        self.session = self.__get_session(self.engine)
        self.positions = []
        self.insert_limit = insert_limit
    

    def __get_engine(self, config):
        try:
            connection_string = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
                config['user'], config['password'], config['host'], config['port'], config['database'])
            return db.create_engine(connection_string, echo=False)
        except db.exc.SQLAlchemyError as err:
            print(err)
    

    def __get_session(self, engine):
        try:
            return Session(engine)
        except db.exc.SQLAlchemyError as err:
            print(err)
    

    def __bulk_insert(self):
        """
        inserts a record list into to db and clears the positions list in the internal object list
        """
        with self.session as session:
            try:
                session.add_all(self.positions)
            except db.exc.SQLAlchemyError as err:
                session.rollback()
                print(err)
            else:
                session.commit()
                self.positions.clear()
    

    def insert(self, p):
        """
        inserts a new position in the internal positions list and writes the list to db if size is large
        @param p: instance of Position class
        """
        if type(p) != Position:
            raise TypeError('Must be of type Position.')
        else:
            self.positions.append(p)

            if (len(self.positions) >= self.insert_limit):
                self.__bulk_insert()
    

    def empty_table(self):
        """
        empties the whole table
        """
      
        with self.session as session:
            try:
                session.query(Position).delete()
            except db.exc.SQLAlchemyError as err:
                session.rollback()
                print(err)
            else:
                session.commit()
    

    def close(self) -> None:
        """
        closes all connections to the database
        """
        with self.session as session:
            session.flush()
            session.close_all()
        with self.engine as engine:
            engine.dispose()
            engine.drop()

    
    def get_unique_session_ids(self) -> list:
        """
        gets all unique session ids from the table
        @return: list of ids as string
        """
        return pd.read_sql_query('SELECT DISTINCT session_id FROM positions;', self.engine)['session_id'].tolist()
    

    def get_session_data(self, session_id) -> DataFrame:
        """
        Get all data of all cfs from a session
        @param session_id: session id as string
        @return: pandas df
        """
        query = "SELECT * FROM positions WHERE session_id='{}';"
        return pd.read_sql_query(query.format(str(session_id)), self.engine)
    
    
    def get_all_cfs_in_session(self, session_id) -> list:
        """
        gets all cfs that are present in a session and returns a list
        @param session_id: session id as string
        @return: list of cfs
        """
        query = """SELECT DISTINCT crazyflie_id
                FROM positions
                WHERE session_id='{}';
                """
        return pd.read_sql_query(query.format(str(session_id)), self.engine)['crazyflie_id'].tolist()


    def get_cfs_data_from_session(self, session_id, crazyflie_ids) -> DataFrame:
        """
        Get data of certains cfs within a session
        @param session_id: session id as string
        @param crazyflie_ids: cf id as string
        @return: pandas df
        """
        cf_ids_param = f'"{crazyflie_ids[0]}"'
        cf_ids_length = len(crazyflie_ids)

        if (cf_ids_length > 1):
            cf_ids_param = ''
            for cf_id in crazyflie_ids:
                if (crazyflie_ids.index(cf_id) != cf_ids_length - 1):
                    cf_ids_param += f'"{cf_id}",'
                else:
                    cf_ids_param += f'"{cf_id}"'

        query = """SELECT * FROM positions
                WHERE session_id='{}'
                AND crazyflie_id IN ({})
                ORDER BY timestamp ASC;
                """
        return pd.read_sql_query(query.format(str(session_id), cf_ids_param), self.engine)

    