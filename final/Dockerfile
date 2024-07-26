FROM ubuntu:latest
LABEL authors="franco"

ENTRYPOINT ["top", "-b"]

# Use a lightweight base image with Python
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt requirements.txt

# Install dependencies
RUN python -m venv /venv && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Set the environment variables for Flask
ENV FLASK_APP=run.py
ENV PATH="/venv/bin:$PATH"

# Command to run the Flask application
CMD ["/venv/bin/flask", "run", "--host=0.0.0.0", "--port=8080"]

