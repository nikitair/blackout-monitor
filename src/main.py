import os
from dotenv import load_dotenv
from pinger import ping_router

load_dotenv()

IP_ADDRESS = os.getenv("IP_ADDRESS", "")

ping_response = ping_router(IP_ADDRESS)

print(ping_response.stdout)