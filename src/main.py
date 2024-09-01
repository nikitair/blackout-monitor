import os
import time
from dotenv import load_dotenv
from pinger import ping_address

load_dotenv()

os.environ['TZ'] = 'UTC'
time.tzset()

IP_ADDRESS = os.getenv("IP_ADDRESS", "")

ping_response = ping_address(IP_ADDRESS)

print(ping_response)
