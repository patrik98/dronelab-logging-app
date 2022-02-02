from sqlalchemy import Column, String, Integer, Float, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Position(Base):
    """
    Position Class to verify the data structure
    @param session_id: Session id as string
    @param crazyflie_id: crazieflie id as string (eg. 'cf1')
    @param x: x position float
    @param y: y position float
    @param z: z position float
    @param timestamp: timestamp as int (secs + nsecs)
    """
    __tablename__ = "positions"

    id = Column(Integer(), primary_key=True)
    session_id = Column(String(255))
    crazyflie_id = Column(String(255))
    x = Column(Float())
    y = Column(Float())
    z = Column(Float())
    ts = Column(BigInteger())

    def __init__(self, session_id, crazyflie_id, x, y, z, ts):
        self.session_id = session_id
        self.crazyflie_id = crazyflie_id
        self.x = x
        self.y = y
        self.z = z
        self.ts = ts

    def __repr__(self):
        return f'Position: {self.id}, {self.session_id}, {self.crazyflie_id}, {self.x}/{self.y}/{self.z}, {self.ts}'

