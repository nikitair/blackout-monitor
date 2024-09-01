import os
import time
import schedule
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
import subprocess
from logging_config import logger
from db import class_connector

load_dotenv()
EMAIL_URL = os.getenv("RETOOL_EMAIL_NOTIFICATION_URL")


class Pinger:
    
    def __init__(self, location_id: int) -> None:
        self.location_id = location_id
        self.ip_address = None
        self.state = None
        self.state_changed_at = None
        self.run = False
        
        
    @class_connector
    def set_location_data(self, con) -> None:
        with con.cursor() as cur:
            cur.execute(
                f"""
                SELECT
                    l.id AS location_id,
                    l.ip,
                    e.state,
                    e.created_at
                FROM
                    events e
                FULL OUTER JOIN locations l ON l.id = e.location_id
                WHERE
                    l.id = {self.location_id}
                ORDER BY
                    e.created_at DESC
                LIMIT 1;
                """
            )
            data = cur.fetchall()
            logger.info(f"sql response data - ({data})")
            if data:
                self.ip_address = data[0][1]
                self.state = data[0][2] if data[0][2] else "connected"
                self.state_changed_at = data[0][3] if data[0][3] else datetime.now(timezone.utc)
            else:
                self.notify("Blackout Monitor Error", "No IP Address Found in database")
                raise ValueError("No IP Address Found in database")


    def ping_address(self) -> dict | None:
        logger.info(f"ping address - ({self.ip_address})")
        try:
            response = subprocess.run(
                ["ping", "-c", "1", self.ip_address],
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
            logger.error(f"!!! exception occurred - ({ex})")
            
        
    def check_electricity(self) -> None:
        if self.ip_address:
            ping_response = self.ping_address(self.ip_address)
        else:
            self.notify("Blackout Monitor Error", "No IP address")
            raise ValueError("!!! no ip address provided")
            
            
    
    def launch_polling(self) -> None:
        logger.info("launch pinger polling")
        schedule.every(10).seconds.do(self.ping_address)
        while self.run is True:
            schedule.run_pending()
            time.sleep(1)
        logger.warning("polling stopped")


    def notify(subject: str, message: str) -> None:
        requests.post(
            url=EMAIL_URL, 
            json={
                "subject": subject,
                "message": message
            }    
        )
