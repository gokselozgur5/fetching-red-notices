# Red Notices Data Fetcher

Red Notices Data Fetcher is a Python application that fetches the red notices data from the Interpol API, then sends it to RabbitMQ message queue and stores it in a PostgreSQL database. It uses the aio_pika and SQLAlchemy libraries to interact with RabbitMQ and PostgreSQL, respectively. The application is designed to be run as a Docker container and can be deployed using Docker Compose.

The application consumes messages from a RabbitMQ message queue using an asynchronous consumer, processes the messages and stores the data in a PostgreSQL database using SQLAlchemy. The application has an HTTP server implemented using FastAPI that serves a basic HTML page with a template engine for rendering dynamic content.

The application also includes functionality to compare the data that has been consumed from RabbitMQ with the data that is stored in the PostgreSQL database. It uses a delta database to store the differences between the two datasets, and provides an API endpoint to retrieve the delta dataset.

The Red Notices Data Fetcher application is designed to be easily customizable and extendable. To Be Continued...

# Table of Contents
1. [Getting Started](#getting-started)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Contributing](#contributing)
6. [License](#license)


# Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

# Prerequisites

    Docker and Docker Compose
    Python 3.8 or higher

# Installation

- Clone the repository

`git clone https://github.com/gokselozgur5/fetching-red-notices.git`

`cd fetching-red-notices`

- Create a .env file with the required environment variables:

```yaml
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=your_database_name
POSTGRES_USER=your_database_user
POSTGRES_PASSWORD=your_database_password
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_VIRTUAL_HOST=/
RABBITMQ_QUEUE_NAME=your_queue_name
```

- Build the Docker image and start the containers

`docker-compose up --build`


# Usage

    The FastAPI application is running on http://localhost:8001/
    The RabbitMQ management interface is running on http://localhost:15672/
    The PostgreSQL database is accessible on port 5432


# Contributing

Contributions are welcome! Please open an issue or submit a pull request to propose changes.

# License

This project is licensed under the MIT License.
