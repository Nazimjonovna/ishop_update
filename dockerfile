# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /ishop_update

# Install dependencies
COPY requirements.txt /ishop_update/
COPY . /ishop_update/
RUN pip install -r requirements.txt

