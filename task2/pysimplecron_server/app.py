import socket
import time
import sqlite3
from pathlib import Path

BASEDIR = BASE_DIR = Path(__file__).parent.absolute()

HOST = '127.0.0.1'
PORT = 9090

SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SOCK.bind((HOST, PORT))
SOCK.listen(1)

DB_PATH = BASEDIR / '.db'
if not (DB_PATH).exists():
    db_conn = sqlite3.connect(DB_PATH)
    c = db_conn.cursor()
    c.execute('''CREATE TABLE jobs 
    (command text, year integer, month integer, day integer, 
    hour integer, minute integer, second integer)''')
    db_conn.commit()
    db_conn.close()


def loop_socket():
    _process = lambda val: 'NULL' if val == '*' else int(val)

    while True:
        print('Waiting...')
        conn, _ = SOCK.accept()

        print('Data recieving...')
        data = conn.recv(1024)
        data = data.decode()

        command, dt = data.split('#')

        print('Processing...')
        date, time = dt.split('T')
        year, month, day = list(map(_process, date.split('-')))
        hour, minute, second = list(map(_process, time.split(':')))

        conn.send(b'Ok!')
        conn.close()

        print('Uploading to db...')
        db_conn = sqlite3.connect(DB_PATH)
        c = db_conn.cursor()
        c.execute(f"INSERT INTO jobs VALUES ('{command}',{year},{month},{day},{hour},{minute},{second})")
        db_conn.commit()
        db_conn.close()

# PID_EXECUTER = None

# def loop_executer():
#     while True:
#         time.sleep(0.5) # To avoid loading the CPU

if __name__ == '__main__':
    loop_socket()