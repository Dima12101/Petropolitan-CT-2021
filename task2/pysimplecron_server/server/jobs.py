import asyncio
import sqlite3
from datetime import datetime

from . import config


def create_jobs_schedule():
    conn = sqlite3.connect(config.JOBS_SCHEDULE_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE jobs 
    (command text, year integer, month integer, day integer, 
    hour integer, minute integer, second integer)''')
    conn.commit()
    conn.close()


def add_job_to_schedule(command, datetime):
    year, month, day, hour, minute, second = datetime
    conn = sqlite3.connect(config.JOBS_SCHEDULE_PATH)
    c = conn.cursor()
    c.execute(f"INSERT INTO jobs VALUES ('{command}',{year},{month},{day},{hour},{minute},{second})")
    conn.commit()
    conn.close()


async def handle_jobs_schedule():
    while True:
        await asyncio.sleep(2)

        datetime_now = datetime.now()
        print('handle_job_queue:', datetime_now)
