import os
import pwd
from server.config import BASEDIR

if __name__ == '__main__':
    with open('/etc/systemd/system/pysimplecron.socket', 'w') as socket_file:
        socket_file.write(
"""[Unit]
Description=PySimpleCron socket

[Socket]
ListenStream=/run/pysimplecron.sock

[Install]
WantedBy=sockets.target""")
    with open('/etc/systemd/system/pysimplecron.service', 'w') as service_file:
        service_file.write(
f"""[Unit]
Description=PySimpleCron daemon service
Requires=pysimplecron.socket
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User={pwd.getpwuid(os.getuid()).pw_name}
ExecStart={BASEDIR / 'venv/bin/python3'} run.py

[Install]
WantedBy=multi-user.target""")