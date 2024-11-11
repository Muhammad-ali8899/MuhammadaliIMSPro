# Base image
FROM python:3.12-slim

# Set working directory in the container
WORKDIR /test

# Copy all project files to the container
COPY . /test/

# Install Poetry for dependency management
RUN pip install poetry

# Install dependencies
RUN poetry install

# Command to run on container start
CMD ["poetry", "run", "python", "test/ims.py"]
