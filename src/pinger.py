import os
from dotenv import load_dotenv
import subprocess
from logging_config import logger

load_dotenv()



def ping_router(ip_address: str):
    logger.info(f"ping address - {ip_address}")
    try:
        ping_response = subprocess.run(
            ["ping", "-c", "1", ip_address],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return ping_response
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    res = ping_router(os.getenv("IP_ADDRESS"))