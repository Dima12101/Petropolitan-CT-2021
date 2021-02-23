import asyncio
import sqlite3
import os
import logging
from datetime import datetime

from . import config


def create_jobs_schedule():
    conn = sqlite3.connect(config.JOBS_SCHEDULE_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE jobs
                 (id INTEGER PRIMARY KEY,
                  command TEXT NOT NULL,
                  datetime TIMESTAMP NOT NULL,
                  uid INTEGER NOT NULL,
                  gid INTEGER NOT NULL)''')
    conn.commit()
    conn.close()


def add_job_to_schedule(command, datetime, uid, gid):
    conn = sqlite3.connect(config.JOBS_SCHEDULE_PATH)
    c = conn.cursor()
    
    values = f"'{command}','{datetime}',{uid},{gid}"
    c.execute(f"INSERT INTO jobs(command,datetime,uid,gid) VALUES ({values})")
    
    conn.commit()
    conn.close()

def _set_cred(uid, gid):
    def wrapper():
        os.setgid(gid)
        os.setuid(uid)
    return wrapper

async def executer_job(command, dt, uid, gid):
    proc = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        preexec_fn=_set_cred(uid, gid))
    
    stdout, stderr = await proc.communicate()

    log = f'[{dt} - {command!r} exited with {proc.returncode}]'
    if stdout: log += f'\n[stdout]\n{stdout.decode()}'
    if stderr: log += f'\n[stderr]\n{stderr.decode()}'
    logging.info(log)

async def handle_jobs_schedule():
    while True:
        await asyncio.sleep(2)  # To avoid loading the CPU

        datetime_now = datetime.now()

        # All jobs that should be started on a schedule
        conn = sqlite3.connect(config.JOBS_SCHEDULE_PATH)
        c = conn.cursor()
        c.execute(f"SELECT * FROM jobs WHERE datetime <= '{datetime_now}'")
        jobs = c.fetchall()
        print(f'handle_jobs_schedule: Active jobs - {len(jobs)}')

        # Run all jobs
        for job in jobs:
            id, command, dt, uid, gid = job

            # Run job
            print(f'handle_jobs_schedule: Run job')
            asyncio.run_coroutine_threadsafe(
                executer_job(command, dt, uid, gid),
                asyncio.events.get_event_loop())

            # Delete job
            c.execute(f"DELETE FROM jobs WHERE id = {id}")
            conn.commit()

        conn.close()
