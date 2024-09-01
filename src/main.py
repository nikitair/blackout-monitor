import os
import time
from dotenv import load_dotenv
from monitor import BlackoutMonitor

load_dotenv()

os.environ['TZ'] = 'UTC'
time.tzset()

monitor = BlackoutMonitor(1)
monitor.launch_polling()
