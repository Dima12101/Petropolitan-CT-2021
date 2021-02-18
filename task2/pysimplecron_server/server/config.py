from pathlib import Path

BASEDIR = BASE_DIR = Path(__file__).parent.parent.absolute()

HOST = '127.0.0.1'
PORT = 9090

JOBS_SCHEDULE_PATH = BASEDIR / 'schedule.db'
