from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pika 
import os
from dotenv import load_dotenv
import logging
import uvicorn
from db_operations import DatabaseManager

try:
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
    load_dotenv(dotenv_path)
except Exception as e:
    # exception object might be more specific
    logging.error(f'environment file could not be loaded! \n{e}')


class RabbitMQConsumer:
    def __init__(self):
        self.host = os.getenv('RABBITMQ_HOST')
        self.port = os.getenv('RABBITMQ_PORT')
        self.username = os.getenv('RABBITMQ_USERNAME')
        self.password = os.getenv('RABBITMQ_PASSWORD')
        self.virtual_host = os.getenv('RABBITMQ_VIRTUAL_HOST')
        self.queue_name = os.getenv('RABBITMQ_QUEUE_NAME')

        self.credentials = pika.PlainCredentials(self.username, self.password)
        self.parameters = pika.ConnectionParameters(self.host,
                                                     self.port,
                                                     self.virtual_host,
                                                     self.credentials, heartbeat=50)
        self.connection = None
        self.channel = None

    def connect(self):
        """Establish a connection to the RabbitMQ server"""
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(self.parameters)
            self.create_channel()
            print('baglandim')

    def create_channel(self):
        """Create a new channel on the existing connection"""
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def consume(self, callback):
        """Consume messages from the RabbitMQ server"""
        self.connect()
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def close(self):
        """Close the connection to the RabbitMQ server"""
        if self.connection and self.connection.is_open:
            self.connection.close()

app = FastAPI()
templates = Jinja2Templates(directory="./templates")
consumer = RabbitMQConsumer()

# Create a DatabaseManager instance and insert the list into the database
manager = DatabaseManager()

@app.on_event("startup")
async def startup():
    consumer.consume(callback)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": f"Red Notices List {request}"})


def callback(ch, method, properties, body):
    print("Received message:", 'hehe')
    print(type(body))
    manager.insert_list_to_table(body)

    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)