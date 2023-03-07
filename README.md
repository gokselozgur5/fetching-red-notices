# Red Notices Data Fetcher
This repository provides a Python script for fetching data about red notices from the Interpol's public API. Red notices are international wanted notices issued by Interpol to alert law enforcement agencies around the world about individuals who are wanted for extradition or prosecution.
Project Title

This project is a sample FastAPI application that consumes messages from a RabbitMQ queue and stores them in a PostgreSQL database. The application can be run using Docker Compose to set up the required services.
Table of Contents

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
