# Stage 1: Build stage
FROM python:3.12-slim as build

# Set environment variables
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file to leverage Docker cache
COPY requirements.txt .

# Create a virtual environment and install dependencies
RUN python3 -m venv $VIRTUAL_ENV \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Stage 2: Final stage
FROM python:3.12-slim as final

# Set the virtual environment path
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set the working directory for the final container
WORKDIR /app

# Copy the virtual environment from the build stage
COPY --from=build /opt/venv /opt/venv

# Copy the application code to the container (excluding unnecessary files)
COPY . .

# Expose the application port
EXPOSE 5000

# Set the environment variables
ENV PYTHONUNBUFFERED=1 FLASK_ENV=prod

# Start the application
CMD ["python", "main.py"]
