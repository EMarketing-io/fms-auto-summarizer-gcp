# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (FFmpeg for audio, plus build tools)
RUN apt-get update && \
    apt-get install -y ffmpeg gcc g++ && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file first (for build cache optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Set Python environment to always flush logs
ENV PYTHONUNBUFFERED=1

# Command to run your application
CMD ["python", "main.py"]
