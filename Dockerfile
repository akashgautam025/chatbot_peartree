# Use an official lightweight Python image.
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt 

# Make port 5051 available to the world outside this container
EXPOSE 5051

# Run app.py using gunicorn when the container launches
CMD ["gunicorn", "app:app", "-w 2", "-k gevent", "-b 0.0.0.0:5051", "--access-logfile", "-", "--error-logfile", "-"]
