# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in Result_Requirements.txt
RUN pip install --no-cache-dir -r Result_Requirements.txt

# Make port 5003 available to the world outside this container
EXPOSE 5003

# Define environment variable
ENV FLASK_APP=ResultsApp.py

# Run the application
CMD ["python", "ResultsApp.py"]