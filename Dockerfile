# Use Python 3.11 as the base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install curl for downloading uv
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy requirements file
COPY requirements.txt .

# Install dependencies using uv
RUN uv pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port your server runs on
EXPOSE 8000

# Start the server
CMD ["python", "run.py"]