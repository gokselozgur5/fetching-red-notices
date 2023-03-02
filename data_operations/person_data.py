import json
import requests
from urllib.parse import urlparse, parse_qs
from time import sleep
import pika
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler

#  Set up logging to a file
log_file = 'fetch-data.log'
log_max_size = 1024 * 1024  # 1 MB
log_backup_count = 5  # Keep up to 5 backup files
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s',
                    handlers=[RotatingFileHandler(log_file, maxBytes=log_max_size, backupCount=log_backup_count)])

#  Loading info from configuration file
try:
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
    load_dotenv(dotenv_path)
    logging.debug(f'{__name__} is started.')
except Exception as e:
    # exception object might be more specific
    logging.error(f'environment file could not be loaded! \n{e}')


class RabbitMQClient:
    """A RabbitMQ client that encapsulates the connection and channel"""

    def __init__(self):
        """Initialize the RabbitMQ connection and channel"""
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
        self.connect()

    def connect(self):
        """Establish a connection to the RabbitMQ server"""
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(self.parameters)
            self.create_channel()

    def create_channel(self):
        """Create a new channel on the existing connection"""
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def send_message(self, message):
        """Send a message to the RabbitMQ server"""
        try:
            self.connect()
            logging.debug('Connection is created')
            self.channel.basic_publish(exchange='',
                                        routing_key=self.queue_name,
                                        body=message)
            logging.debug('Publish operation is done.')
        except pika.exceptions.AMQPError as p:
            logging.error(f'Error while trying to make a connection \n{p}')
            self.connection.close()
            self.channel = None


def fetch_data():

    api_url = "https://ws-public.interpol.int/notices/v1/red"
    start_page = 1
    result_per_page = 100
    params={
        'resultPerPage': result_per_page,
        'page': start_page,
    }
    headers = {}
    try:
        logging.debug('Fetching data is started.')
        response = requests.request("GET", api_url, headers=headers, params=params)
        if response.ok:
            logging.debug('Fetch operation is successful.')
            data = response.json()
            total_page_url = data['_links']['last']['href']
            records = {}
            records[start_page]= data['_embedded']['notices']
            parsed_url = urlparse(total_page_url)
            query_params = parse_qs(parsed_url.query)
            total_page_number = int(query_params['page'][0])
            for i in range(start_page + 1, total_page_number + 1):
                response = requests.request("GET", api_url, headers=headers, params=params)
                records[i]= data['_embedded']['notices']
            print(type(records))
            record_data = json.dumps(records)
            return record_data
    except Exception as e:
        #  Exceptions can be specified instead of Exception
        logging.error(f'{e}')


if __name__ == '__main__':

    client = RabbitMQClient()
    logging.debug('Client is initiated.')
    fetch_interval = int(os.getenv('FETCH_INTERVAL_SECONDS'))

    while True:
        try:
            records = fetch_data()
            client.send_message(records)
            logging.debug('Datas sent to queue')
        #  Might be declared specific exceptions insted of Exception
        except Exception as e:
            logging.warning(f'{e}')
        #  specified_time (datetime.now() + interval) < datetime.now() as interval instead of sleep
        logging.debug('Interval time... Waiting...')
        sleep(fetch_interval)
