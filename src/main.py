import os
import time
from dotenv import load_dotenv
from pinger import BlackoutMonitor

load_dotenv()

os.environ['TZ'] = 'UTC'
time.tzset()

pinger = BlackoutMonitor(1)
print(pinger.__dict__)

pinger.set_location_data()
print(pinger.__dict__)



