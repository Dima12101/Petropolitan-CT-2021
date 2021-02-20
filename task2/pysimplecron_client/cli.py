import click
import socket
import re

HOST = '127.0.0.1'
PORT = 9090

def send_to_server(command, time):
    # Connecting with server
    print('send_to_server: Connecting...')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_PASSCRED, 1)
    try:
        sock.connect((HOST, PORT))
    except ConnectionRefusedError:
        print('The server is not available!')
        return

    # Sending data to server
    print('send_to_server: Sending...')
    sock.send((command+'#'+time).encode('utf-8'))

    # Waiting answer from server
    print('send_to_server: Waiting...')
    response = sock.recv(1024).decode()
    sock.close()

    if response != 'ERROR':
        print('The job was successfully added to the schedule!')
    else:
        print('An error occurred!')


def validate_time(time):
    pattern = re.compile(r'^([0-9]{4})\-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2}):([0-9]{2})$')
    return pattern.search(time) is not None

@click.command()
@click.option("-c", "--command", help="Shell command which will be run.")
@click.option("-t", "--time", 
help="The time at which the command will be run. Format YYYY-MM-DD hh:mm:ss.")
def main(command, time):
    '''Example call: python cli.py -c "ls ." -t "2021-02-19 14:20:00"'''
    if validate_time(time):
        send_to_server(command, time)
    else:
        print('Time format is not valid!')
    
if __name__ == '__main__':
    main()
