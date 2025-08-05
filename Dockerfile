# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the project files
COPY . .

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1

# Run the main script
CMD ["python", "main.py"]
