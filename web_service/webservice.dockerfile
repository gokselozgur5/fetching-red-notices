# Use the official Python image as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /web_service

# Copy the requirements file into the container and install the dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY /web_service .

# Expose the port that the application will run on
EXPOSE 8001

# Start the application when the container starts
# CMD ["/usr/local/bin/uvicorn", "web_manager:app", "--host", "0.0.0.0", "--port", "8001"]
CMD ["/usr/local/bin/python3", "web_manager.py"]






