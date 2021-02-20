from pathlib import Path
import logging

BASEDIR = BASE_DIR = Path(__file__).parent.parent.absolute()

SOCK_FILE = '/tmp/pysimplecron.sock'

JOBS_SCHEDULE_PATH = BASEDIR / 'schedule.db'

JOBS_LOG_FILE = BASEDIR / 'logs' / 'jobs.log'
logging.basicConfig(
    filename=JOBS_LOG_FILE,
    filemode='a',
    format='%(asctime)s - %(message)s',
    level=logging.INFO)
