from sqlalchemy import Column, String, Integer, Float
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

    id = Column(Integer, primary_key=True)
    session_id = Column(String(255))
    crazyflie_id = Column(String(255))
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    timestamp = Column(Integer)

