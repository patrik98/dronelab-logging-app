import plotly.express as px
import sqlalchemy
import pandas as pd


def create_3d_plot(data):
    """
    creates a 3D scatter plot for a PoseStamp ros-topic
    @param bag_path: the path to the rosbag file
    @param topic_oi: the topic name of interes
    @param cf_id: crazyflie id
    @return: a 3D plotly figure
    """
    fig = px.line_3d(data, x="x", y="y", z="z", color="crazyflie_id")
    return fig


class DBHelper:
    def __init__(self):
        """
        initializes the Helper object be defining the database location
        @param db_name: the name/path to the database as string
        """
        self._config = {
            "user": "cs",
            "pw": "cs123",
            "host": "mysql",
            "port": 3306,
            "db": "cs_db"
        }
        connection_string = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
            self._config['user'],
            self._config['pw'],
            self._config['host'],
            self._config['port'],
            self._config['db'])

        self._engine = sqlalchemy.create_engine(connection_string)

    def get_session_data(self, session_id):
        """
        returns all data that was created within a certain session
        @param session_id: the session id of interest
        @return:
        """
        res = pd.read_sql_query('SELECT * FROM positions WHERE session_id={};'.format(session_id), self._engine)

        return res

    def get_unique_session_ids(self):
        """
        all unique session ids present in the database
        @return:
        """
        session_ids = pd.read_sql_query('SELECT DISTINCT session_id FROM positions;', self._engine)[
            'session_id'].tolist()
        return session_ids

    @staticmethod
    def to_integer(dt_time):
        """
        returns an integer for a given instance of type datetime
        @param dt_time: a datetime instance
        @return: integer (eg. 20211231 for new year)
        """
        return 10000 * dt_time.year + 100 * dt_time.month + dt_time.day

    def get_latest_session_id(self):
        """
        Gets the latest session id available in the database
        @return: instance of class SessionID
        """
        all_session_ids = [SessionID(id_oi) for id_oi in self.get_unique_session_ids()]
        if not all_session_ids:
            return 0
        else:
            return sorted(all_session_ids)[-1]

    def get_all_cfs_in_session(self, session_id):
        """
        queries all cfs that were active within one session
        @param session_id: session_id as a string(caution!)
        @return: a list of cf ids
        """
        session_id = str(session_id)
        res = pd.read_sql_query(
            "SELECT DISTINCT crazyflie_id FROM positions WHERE session_id={}".format(session_id),
            self._engine
        )

        res = res['crazyflie_id'].tolist()

        return res

    def get_cfs_data_from_session(self, session_id, crazyflie_ids):
        """
        quries all data within a session for a selected list of cfs
        @param session_id: session id as string (caution!)
        @param cf_list: a list with strings of cf ids
        @return a pandas df with all cols
        """
        cf_ids_param = f'"{crazyflie_ids[0]}"'
        cf_ids_length = len(crazyflie_ids)

        if cf_ids_length > 1:
            cf_ids_param = ''
            for cf_id in crazyflie_ids:
                if crazyflie_ids.index(cf_id) != cf_ids_length - 1:
                    cf_ids_param += f'"{cf_id}",'
                else:
                    cf_ids_param += f'"{cf_id}"'

        query = f"""SELECT * FROM positions
                        WHERE session_id='{session_id}'
                        AND crazyflie_id IN ({cf_ids_param})
                        ORDER BY timestamp ASC;
                        """
        res = pd.read_sql_query(query, self._engine)
        return res


class SessionID:
    def __init__(self, id_string=None):
        """
        init of a sessionid object (consisting of the date + running number)
        @param id_string: a string with the above mentioned convention
        """
        self.id_string = id_string

    def __lt__(self, other):
        """
        build in method to compare if the current SessionID instance is lower (not more recent) than another instance
        @param other: Instance of SessionID
        @return: True if lower else False
        """
        # if the dates are not equal, the date is sufficient as comparison
        if int(other.get_date()) < int(self.get_date()):
            return False
        elif int(other.get_date()) > int(self.get_date()):
            return True

        # else we have to compare the session number
        else:
            if int(other.get_sess_num()) <= int(self.get_sess_num()):
                return False
            elif int(other.get_sess_num()) < int(self.get_sess_num()):
                return True

    def __eq__(self, other):
        """
        build in method to compare if the current SessionID instance is the same as another instance
        @param other: Instance of SessionID
        @return: True if same else False
        """
        if other.id_string == self.id_string:
            return
        else:
            return False

    def get_following_id(self):
        """
        returns the session id of the consecutive session
        @return: SessionID instance
        """
        date = self.get_date()
        num = str(int(self.get_sess_num()) + 1)
        return SessionID(id_string=date + num)

    def create_sess_id(self, date, sess_num):
        """
        inserts the session id string for the object based on the date and a session number
        @param date:
        @param sess_num:
        """
        self.id_string = date + sess_num

    def get_date(self):
        """
        returns the date part of the id string
        @return: a string
        """
        return self.id_string[0:8]

    def get_sess_num(self):
        """
        returns the session number from the id string
        @return: a string with the number
        """
        return self.id_string[8:]

db = DBHelper()
print(db.get_unique_session_ids())