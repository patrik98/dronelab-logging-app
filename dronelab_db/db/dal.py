from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import pandas as pd
from models.models import Base, Position

class DataAccessLayer():
    def __init__(self):
        self.engine = None
        self.Session = None
        self.metadata = None
        self.positions_to_insert = []
        self.insert_limit = 16


    def connect(self, conn_string, insert_limit = 16):
        '''
        Builds engine and Session class for app layer

        Example config:
        {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'user',
            'password': 'pw',
            'database': 'db'
        }

        Example conn_string:
        conn_string = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
            config['user'], config['password'], config['host'], config['port'], config['database'])
        """
        '''
        self.engine = create_engine(conn_string, echo=False)
        self.metadata = Base.metadata
        self.create_all()
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self.insert_limit = insert_limit


    def bulk_insert(self, records):
        """
        performs a bulk insert on a list of records 
        
        Arguments:
            records {list} -- obj records in list of dicts format 
        """
        session = self.Session()
        with session.begin():
            session.add_all(records)
    

    def insert(self, p):
        """
        inserts a new position in the internal positionsToInsert list and writes the list to db if size is large
        @param p: instance of Position class
        """
        if type(p) != Position:
            raise TypeError('Must be of type Position.')
        else:
            self.positions_to_insert.append(p)

            if (len(self.positions_to_insert) >= self.insert_limit):
                self.bulk_insert(self.positions_to_insert)
                self.positions_to_insert.clear()
    
    def create_all(self):
        self.metadata.create_all(self.engine)
    
    def reset_db(self):
        """
        destroys the database
        """
        self.metadata.drop_all(self.engine)


    def drop_table(self, Model):
        """
        Attempts to drop the specified table from db 
        """
        Model.__table__.drop(self.engine)


    def get_unique_session_ids(self) -> list:
        """
        gets all unique session ids from the table
        @return: list of ids as string
        """
        return pd.read_sql_query('SELECT DISTINCT session_id FROM positions;', self.engine)['session_id'].tolist()
    

    def get_session_data(self, session_id) -> pd.DataFrame:
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
        query = """SELECT DISTINCT crazyflie_id, ts
                FROM positions
                WHERE session_id='{}'
                ORDER BY ts ASC;
                """
        return pd.read_sql_query(query.format(str(session_id)), self.engine)['crazyflie_id'].tolist()


    def get_cfs_data_from_session(self, session_id, crazyflie_ids) -> pd.DataFrame:
        """
        Get data of certains cfs within a session
        @param session_id: session id as string
        @param crazyflie_ids: cf ids as list of strings
        @return: pandas df
        """
        cf_ids_length = len(crazyflie_ids)
        cf_ids_param = ''
        
        if (cf_ids_length == 1):
            cf_ids_param = f'"{crazyflie_ids[0]}"'
  
        elif (cf_ids_length > 1):
            for cf_id in crazyflie_ids:
                if (crazyflie_ids.index(cf_id) != cf_ids_length - 1):
                    cf_ids_param += f'"{cf_id}",'
                else:
                    cf_ids_param += f'"{cf_id}"'

        query = """SELECT * FROM positions
                WHERE session_id='{}'
                AND crazyflie_id IN ({})
                ORDER BY ts ASC;
                """
        return pd.read_sql_query(query.format(str(session_id), cf_ids_param), self.engine)

dal = DataAccessLayer()