import asyncio
import sys

from . import config
from .jobs import create_jobs_schedule, handle_jobs_schedule, add_job_to_schedule

sys.path.append(config.BASE_DIR)


async def handle_client(reader, writer):
    print('handle_client: START')
    
    # Recieve data from client
    print('handle_client: Recieving...')
    data = await reader.read(100)
    data = data.decode()

    # ====== Processing data ======
    print('handle_client: Processing...')
    command, dt = data.split('#')

    _process = lambda val: 'NULL' if val == '*' else int(val)
    
    # TODO: Валидация
    date, time = dt.split('T')
    year, month, day = list(map(_process, date.split('-')))
    hour, minute, second = list(map(_process, time.split(':')))
    # =============================

    # Response to client
    print('handle_client: Response...')
    writer.write(b'Ok!') # TODO: Добавить сообщение об ошибке
    await writer.drain()
    writer.close()

    # Adding job to schedule
    print('handle_client: Adding job to schedule...')
    add_job_to_schedule(command, (year, month, day, hour, minute, second))

    print('handle_client: END')


''' =============== RUN PYSIMPLECRON SERVER ==============='''
def run():
    loop = asyncio.get_event_loop()

    # Register socket-server coroutine
    server_coro = asyncio.start_server(handle_client, config.HOST, config.PORT, loop=loop)
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
