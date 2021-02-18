import click
import socket

HOST = '127.0.0.1'
PORT = 9090

@click.command()
@click.option("-c", "--command", help="Shell command which will be run.")
@click.option("-t", "--time", 
help="The time at which the command will be run. Format YYYY-MM-DD hh:mm:ss. If '*' is specified, it means 'every'")
def main(command, time):

    print('Connecting...')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    print(command)
    print(time)
    
    print('Sending...')
    sock.send((command+'#'+time).encode('utf-8'))
    #sock.send(('D'+time).encode('utf-8'))

    print('Waiting...')
    response = sock.recv(1024).decode()
    sock.close()

    print(response)

if __name__ == '__main__':
    main()

#python app.py -c "ls ." -t "2021-02-*T*:20:00"