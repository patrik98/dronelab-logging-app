import random
import time
from sqlalchemy.orm import Session
from dronelab_db.db.dal import dal
from dronelab_db.models.models import Position

scenario = {
    'session_ids': ['20220202-1', '20220202-2', '20220202-3'],
    'agents_per_session': 9,
    'sent_positions_per_agent': 5
}

dal.connect('sqlite:///:memory:')
session = Session(dal.engine)
 
# prep db, fill with randomly generated cf positions
positions = []
for s in scenario['session_ids']:
    for i in range(scenario['agents_per_session']):
        for j in range(scenario['sent_positions_per_agent']):
            p = Position(session_id=s, crazyflie_id='cf' + str(i+1), x=random.uniform(0, 10), y=random.uniform(0, 10), z=random.uniform(0,3.3), ts=time.time_ns())
            positions.append(p)

with session.begin():
    session.add_all(positions)

print('In-memory database prepared.')