# Pull python image
FROM python:3.11.0-slim-bullseye

# Set Environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt /code/
RUN pip install -r requirements.txt

# Copy project
COPY . /code/




