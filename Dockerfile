FROM python:3

# Copy current working directory into the container
COPY . /hackernews

# Make the directory the working directory
WORKDIR /hackernews

# Provision the container with the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run all unit tests
RUN python -m unittest
