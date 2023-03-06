from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pika 
import os
from dotenv import load_dotenv
import logging

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
                                                     self.credentials)
        self.connection = None
        self.channel = None

    def connect(self):
        """Establish a connection to the RabbitMQ server"""
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(self.parameters)
            self.create_channel()

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

@app.post('/api/v1/red-notices-list')
async def post_data(data_list: dict):
    return data_list

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": f"Red Notices List {request}"})

def callback(ch, method, properties, body):
    print("Received message:", body)

if __name__ == '__main__':
    consumer = RabbitMQConsumer()
    consumer.consume(callback)
    consumer.close()