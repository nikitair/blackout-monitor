import os
import time
import zoneinfo
import schedule
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
import subprocess
from logging_config import logger
from db import class_connector

load_dotenv()
EMAIL_URL = os.getenv("RETOOL_EMAIL_NOTIFICATION_URL")


class BlackoutMonitor:
    
    def __init__(self, location_id: int) -> None:
        self.location_id = location_id
        self.ip_address = None
        self.blackout = False
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
                self.blackout = data[0][2] == "disconnected"
                self.state_changed_at = data[0][3] if data[0][3] else datetime.now(timezone.utc)
            else:
                self.notify_admin("Blackout Monitor Error", "No IP Address Found in database")
                raise ValueError("No IP Address Found in database")


    def ping_address(self) -> dict | None:
        logger.info(f"ping address - ({self.ip_address})")
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
                self.notify_admin("Blackout Monitor Error", f"Pinger Error - ({error})")
                raise ValueError("Pinger Error - ({error})")
        else:
            logger.info("success")

        return {
            "blackout": status_code != 0,
            "status_code": status_code,
            "message": message,
            "error": error
        }
        
        
    def check_electricity(self) -> None | str:
        if not self.ip_address:
            self.notify_admin("Blackout Monitor Error", "No IP address")
            raise ValueError("!!! no ip address provided")
        
        ping_response = self.ping_address(self.ip_address)
            
        state_blackout = self.blackout
        blackout = ping_response["blackout"]
        
        if state_blackout != blackout:
            event_message = None
            period = self.calculate_time_period(state_blackout, blackout)
            
            match state_blackout:
                case True:
                    event_message = f"🔋 Дали свет\n(не было {period[0]} час. {period[1]} мин.)"
                case False:
                    event_message = f"🪫 Отключили свет\n(был {period[0]} час. {period[1]} мин.)"
                    
            self.blackout = blackout
            self.state_changed_at = datetime.now(timezone.utc)
            self.save_event_to_db()
                    
            return event_message
            

    @staticmethod
    def calculate_time_period(t_start, t_now) -> tuple:
        time_diff = t_now - t_start
        hours, remainder = divmod(time_diff.total_seconds(), 3600)
        minutes, _ = divmod(remainder, 60)
        return hours, minutes
    
    
    @class_connector
    def save_event_to_db(self, con):
        logger.info("saving event to db")
        event = {
            True: "disconnected",
            False: "connected"
        }
        with con.cursor() as cur:
            cur.execute(
                f"""
                INSERT INTO events
                (
                    location_id,
                    state
                ) 
                VALUES
                (
                    {self.location_id},
                    {event[self.blackout]}
                );
                """
            )
            

    def launch_polling(self) -> None:
        logger.info("launch pinger polling")
        schedule.every(10).seconds.do(self.ping_address)
        while self.run is True:
            schedule.run_pending()
            time.sleep(1)
        logger.warning("polling stopped")


    def notify_admin(subject: str, message: str) -> None:
        requests.post(
            url=EMAIL_URL, 
            json={
                "subject": subject,
                "message": message
            }    
        )
