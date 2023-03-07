import asyncio
import json
from time import sleep
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import aio_pika
import os
from dotenv import load_dotenv
import logging
import uvicorn
from db_operations import DatabaseManager
import pika

try:
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
    load_dotenv(dotenv_path)
except Exception as e:
    # exception object might be more specific
    logging.error(f'environment file could not be loaded! \n{e}')




async def consume_messages() -> None:
    logging.basicConfig(level=logging.DEBUG)
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@rabbitmq:5672//", virtualhost='/'
    )

    queue_name = "red-notices-queue"

    async with connection:
        # Creating channel
        channel = await connection.channel()

        # Will take no more than 10 messages in advance
        await channel.set_qos(prefetch_count=10)

        # Declaring queue
        queue = await channel.declare_queue(queue_name)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    logging.debug(f"{type(message.body)}--------------heheeeeey")
                    convert_byte = message.body.decode('utf8').replace("'", '"')
                    json_data = json.loads(convert_byte)
                    dump_data = json.dumps(json_data, indent=2, sort_keys=True)
                    
                    
                    # Create a DatabaseManager instance and insert the list into the database
                    manager = DatabaseManager()

                    db_test = manager.insert_list_to_table(dump_data)
                    logging.debug(f'{db_test}')
                    message.ack()
                    


                    if queue.name in message.body.decode():
                        break


app = FastAPI()
templates = Jinja2Templates(directory="./templates")


# queue = asyncio.Queue()
# consumer = RabbitMQConsumer(queue=queue)



@app.on_event("startup")
async def startup():
    app.consumer_task = asyncio.create_task(consume_messages())


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": f"Red Notices List {request}"})


def callback(ch, method, properties, body):
    print("Received message:", 'hehe')
    print('hehehehehehehehehehe')
    
    data = json.loads(convert_byte)
    dump_data = json.dumps(data, indent=4, sort_keys=True)
    print('hohohoho')
    


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8001)
