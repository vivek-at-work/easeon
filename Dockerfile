# Pull a base image
FROM python:3.8-slim-buster
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Create a working directory for the django project
WORKDIR /code
# Copy requirements to the container
COPY Pipfile Pipfile.lock /code/
# Install the requirements to the container
RUN pip install pipenv && pipenv install --system
RUN apt-get update  &&  apt-get install -y build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# Copy the project files into the working directory
COPY . /code/
# Open a port on the container
EXPOSE 8000