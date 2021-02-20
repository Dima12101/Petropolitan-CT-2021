from pathlib import Path

BASEDIR = BASE_DIR = Path(__file__).parent.parent.absolute()

SOCK_FILE = '/tmp/pysimplecron.sock'

JOBS_SCHEDULE_PATH = BASEDIR / 'schedule.db'
