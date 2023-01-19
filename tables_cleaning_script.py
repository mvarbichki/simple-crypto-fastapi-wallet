from dotenv import load_dotenv
from os import environ as env
from mysql.connector import connect, Error
from datetime import datetime


# load .env file
load_dotenv()
# set timestamp
dt = datetime.now()


# appending messages to logs.txt
def append_to_logs(log_msg, err=None):
    with open("logs.txt", "a") as f:
        if log_msg == "ERROR":
            f.write(f"\n{dt} | {log_msg}: {err}")
        else:
            f.write(f"\n{dt} | {log_msg}: TABLES TRUNCATED SUCCESSFULLY")


# cleans tables content
def wipe_tables_content():
    # handle issues
    try:
        connection = connect(
            user=env.get("MYSQL_USER"),
            password=env.get("MYSQL_PASSWORD"),
            host=env.get("MYSQL_HOST"),
            port=env.get("MYSQL_PORT"),
            database=env.get("MYSQL_DATABASE")
        )

        cursor = connection.cursor()

        cursor.execute("truncate table crypto;")
        cursor.execute("truncate table activities;")

        connection.commit()

        cursor.close()
        connection.close()

        # writes a successful message into logs.txt
        append_to_logs("DONE")

    except Error as e:
        # writes error message into logs.txt
        append_to_logs("ERROR", e)


wipe_tables_content()
