# Use the official Python image as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /data_operations

# Copy the requirements file into the container and install the dependencies
COPY ../requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY /data_operations .

# Start the application when the container starts
CMD ["python3", "person_data.py"]