import os
from dotenv import load_dotenv
import psycopg
from psycopg.errors import (SyntaxError as PostgresSyntaxError, 
                            OperationalError as PostgresOperationalError, 
                            ProgrammingError as PostgresProgrammingError)
from logging_config import logger

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 0))
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")


CONNECTION_STRING = f"""
    dbname={POSTGRES_DATABASE} 
    user={POSTGRES_USER} 
    host={ POSTGRES_HOST} 
    port={POSTGRES_PORT} 
    password={POSTGRES_PASSWORD}
    sslmode=require
"""


# with psycopg.connect(CONNECTION_STRING) as conn:
#     with conn.cursor() as cur:
#         cur.execute(
#             """
#             SELECT * FROM locations;
#             """
#         )
#         data = cur.fetchall()
#         print(data)

def connector(sql_query):
    def wrapper(*args, **kwargs):
        try:
            with psycopg.connect(CONNECTION_STRING) as conn:
                logger.info("successful postgres connection")
                return sql_query(conn, *args, **kwargs)
        except PostgresSyntaxError as ex:
            logger.error(f"!!! postgres syntax error occurred - ({ex})")
        except PostgresOperationalError as ex:
            logger.error(f"!!! failed postgres connection - ({ex})")
        except PostgresProgrammingError as ex:
            logger.error(f"!!! other postgres error occurred - ({ex})")
        except Exception as ex:
            logger.exception(f"!!!! unexpected exception occurred - ({ex})")
    return wrapper


def class_connector(sql_query):
    def wrapper(self, *args, **kwargs):
        try:
            with psycopg.connect(CONNECTION_STRING) as conn:
                logger.info("successful postgres connection")
                return sql_query(self, conn, *args, **kwargs)
        except PostgresSyntaxError as ex:
            logger.error(f"!!! postgres syntax error occurred - ({ex})")
        except PostgresOperationalError as ex:
            logger.error(f"!!! failed postgres connection - ({ex})")
        except PostgresProgrammingError as ex:
            logger.error(f"!!! other postgres error occurred - ({ex})")
        except Exception as ex:
            logger.exception(f"!!!! unexpected exception occurred - ({ex})")
    return wrapper


@connector
def check_connection(con):
    with con.cursor() as cur:
        cur.execute("SELECT 1=1;")
        data = cur.fetchall()
        return data


if __name__ == "__main__":
    check_connection()
