# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in Entry_Requirements.txt
RUN pip install --no-cache-dir -r Entry_Requirements.txt

# Make port 5002 available to the world outside this container
EXPOSE 5002

# Define environment variable
ENV FLASK_APP=DataEntry.py

# Run the application
CMD ["python", "DataEntry.py"]