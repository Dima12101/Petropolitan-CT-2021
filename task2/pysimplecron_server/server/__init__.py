import asyncio
import socket
import struct
from datetime import datetime

from . import config
from .jobs import create_jobs_schedule, handle_jobs_schedule, add_job_to_schedule


async def handle_client(reader, writer):
    print('handle_client: START')
    
    # Recieve data from client
    print('handle_client: Recieving...')
    data = await reader.read(100)
    data = data.decode()

    sock = writer.transport.get_extra_info("socket")
    creds = sock.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize('3i'))
    _, uid, gid = struct.unpack('3i', creds)

    # ====== Processing data ======
    print('handle_client: Processing...')
    command, dt = data.split('#') # TODO: Не безопасное разделение

    try:
        dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        print('handle_client: Response ERROR...')
        writer.write(b'ERROR')
        await writer.drain()
        writer.close()
    # =============================

    # Response OK to client
    print('handle_client: Response OK...')
    writer.write(b'OK')
    await writer.drain()
    writer.close()

    # Adding job to schedule
    print('handle_client: Adding job to schedule...')
    add_job_to_schedule(command, dt)

    print('handle_client: END')


''' =============== RUN PYSIMPLECRON SERVER ==============='''
def run():
    loop = asyncio.get_event_loop()

    # Register socket-server coroutine
    server_coro = asyncio.start_unix_server(handle_client, config.SOCK_FILE, loop=loop)
    server = loop.run_until_complete(server_coro)
    print('Servier on {}'.format(server.sockets[0].getsockname()))

    if not config.JOBS_SCHEDULE_PATH.exists(): create_jobs_schedule()
    # Register handle of jobs's schedule coroutine
    h_jobs_schedule = loop.create_task(handle_jobs_schedule())

    # Run loop
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close all
    h_jobs_schedule.cancel()
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
