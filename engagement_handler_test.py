
import sys, logging
from robot_manager.pepper.handler.connection_handler import ConnectionHandler

from robot_manager.pepper.handler.engagement_handler import EngagementHandler

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s %(filename)s:%(lineno)4d: %(message)s",
                    stream=sys.stdout)

s = ConnectionHandler.create_qi_session("192.168.0.119", 9559)
eh = EngagementHandler(s)
eh.subscribe()

print(eh.people_in_zones)
