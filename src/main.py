import os
import time
from dotenv import load_dotenv
from pinger import ping_address
from pinger import Pinger

load_dotenv()

os.environ['TZ'] = 'UTC'
time.tzset()

# IP_ADDRESS = os.getenv("IP_ADDRESS", "")

# ping_response = ping_address(IP_ADDRESS)

# print(ping_response)

pinger = Pinger(1)
print(pinger.__dict__)

pinger.set_location_data()
print(pinger.__dict__)



