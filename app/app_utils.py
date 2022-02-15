import plotly.express as px
import numpy as np
from dronelab_db.data.dal import DataAccessLayer
from dronelab_db.models.position import Position

def create_3d_plot(data):
    """
    creates a 3D scatter plot for a PoseStamp ros-topic
    @param bag_path: the path to the rosbag file
    @param topic_oi: the topic name of interes
    @param cf_id: crazyflie id
    @return: a 3D plotly figure
    """
    fig = px.line_3d(data,
                     x="x",
                     y="y",
                     z="z",
                     color="crazyflie_id",
                     labels={
                         "crazyflie": "crazyflie_id", "time": "timestamp"
                     }
                     )
    return fig


class DBHelper:
    def __init__(self):
        """
        initializes the Helper object be defining the database location
        @param config: dictionary with the database connection config.
                       example:
            {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'user',
            'password': 'pw',
            'database': 'db'
            }
        """
        config = {
            "user": "cs",
            "password": "cs123",
            "host": "mysql",
            "port": 3306,
            "database": "cs_db"
        }
        conn_string = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
        config['user'], config['password'], config['host'], config['port'], config['database'])
        self.db = DataAccessLayer(conn_string=conn_string, insert_limit=16)

    def get_session_data(self, session_id):
        """
        returns all data that was created within a certain session
        @param session_id: the session id of interest
        @return:
        """
        return self.db.get_session_data(session_id)

    def get_unique_session_ids(self):
        """
        all unique session ids present in the database
        @return: the session ids as a list of strings
        """
        return self.db.get_unique_sessions()

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
        return self.db.get_all_cfs_in_session(session_id)

    def get_cfs_data_from_session(self, session_id, crazyflie_ids):
        """
        quries all data within a session for a selected list of cfs
        @param session_id: session id as string (caution!)
        @param cf_list: a list with strings of cf ids
        @return a pandas df with all cols
        """
        return self.db.get_cfs_data_from_session(session=session_id, crazyflie_ids=crazyflie_ids)

    def create_mock_session(self):
        cf_id = 1000 * ["cf1"]
        session_id = 1000 * ["202202091"]
        timestamp = 123456789 + np.linspace(0, 10000, 1000, dtype="uint")
        x = []
        y = []
        z = []
        for i in range(1000):
            z.append(i*0.01)
            x.append(np.cos(i/100 * np.pi))
            y.append(np.sin(i / 100 * np.pi))

        for i in range(1000):
            self.db.insert(Position(session_id=session_id[i],
                                    crazyflie_id=cf_id[i],
                                    x=x[i],
                                    y=y[i],
                                    z=z[i],
                                    timestamp=int(timestamp[i])))


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
            elif int(other.get_sess_num()) > int(self.get_sess_num()):
                return True

    def __eq__(self, other):
        """
        build in method to compare if the current SessionID instance is the same as another instance
        @param other: Instance of SessionID
        @return: True if same else False
        """
        if other.id_string == self.id_string:
            return True
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
        @param date: date as string
        @param sess_num: string
        """

        # test if string consists of integegers
        try:
            int(date)
        except ValueError:
            raise ValueError("the date should be a string of 8 integers!")

        if len(date) != 8:
            raise ValueError("the date should be a string of 8 integers!")

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





