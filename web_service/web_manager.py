import asyncio
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import aio_pika
import os
from dotenv import load_dotenv
import logging
import uvicorn
from db_operations import DatabaseManager

#  TODO: Refactoring


try:
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
    load_dotenv(dotenv_path)

except Exception as e:
    # exception object might be more specific
    logging.error(f'environment file could not be loaded! \n{e}')

#  No need to error handling
#  Because It will take the second parameter If data is not provided.
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USERNAME = os.getenv('RABBITMQ_USERNAME', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')
RABBITMQ_VIRTUAL_HOST = os.getenv('RABBITMQ_VIRTUAL_HOST', '/')
RABBITMQ_QUEUE_NAME = os.getenv('RABBITMQ_QUEUE_NAME', 'red-notices-queue')
DISPLAY_DATA = ""


#  TODO: Make the function Class Object
async def consume_messages() -> None:
    global DISPLAY_DATA
    logging.basicConfig(level=logging.DEBUG)
    connection = await aio_pika.connect_robust(
        f"amqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//", virtualhost=RABBITMQ_VIRTUAL_HOST
    )
    async with connection:
        # Creating channel
        channel = await connection.channel()

        # Will take no more than 1 messages in advance
        await channel.set_qos(prefetch_count=1)

        # Declaring queue
        queue = await channel.declare_queue(RABBITMQ_QUEUE_NAME)

        # Taking item by iterating queue
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    logging.debug(f"{type(message.body)}--------------heheeeeey")
                    convert_byte = message.body.decode('utf8').replace("'", '"')
                    json_data = json.loads(convert_byte)
                    dump_data = json.dumps(json_data, indent=2, sort_keys=True)
                    # Create a DatabaseManager instance and insert the list into the database
                    manager = DatabaseManager()
                    logging.warning(f"-----------{type(json_data)}")
                    manager.insert_list_to_table(json_data)
                    # db_data = manager.get_items_from_table()
                    DISPLAY_DATA = dump_data
                    message.ack()
                    if queue.name in message.body.decode():
                        break


app = FastAPI()
templates = Jinja2Templates(directory="./templates")


async def start_background_tasks():
    loop = asyncio.get_running_loop()
    while True:
        task = loop.create_task(consume_messages())
        await task



@app.on_event("startup")
async def startup():
    loop = asyncio.get_event_loop()
    loop.create_task(start_background_tasks())
    logging.warning('run forever')



@app.on_event('shutdown')
async def shutdown_event():
    app.app_bg_task.cancel()
    await app.app_bg_task

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "data": DISPLAY_DATA, "title": f"Red Notices List {request}"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
