import os
from dotenv import load_dotenv
import subprocess
from logging_config import logger

load_dotenv()


def ping_address(ip_address: str) -> dict | None:
    logger.info(f"ping address - ({ip_address})")
    try:
        response = subprocess.run(
            ["ping", "-c", "1", ip_address],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        status_code = response.returncode
        message = response.stdout.decode()
        error = response.stderr.decode()
        
        logger.info(f"ping status code - ({status_code})")
        logger.info(f"ping message - ({message})")
        
        if status_code != 0:
            if not error:
                logger.warning(f"!!! blackout")
            else:
                logger.error(f"! error - ({error})")
        else:
            logger.info("success")

        return {
            "blackout": status_code != 0,
            "status_code": status_code,
            "message": message,
            "error": error
        }
    except Exception as ex:
        logger.error(f"!!! error occurred - ({ex})")


if __name__ == "__main__":
    res = ping_address(os.getenv("IP_ADDRESS"))