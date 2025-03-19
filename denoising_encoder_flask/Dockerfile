# Use Python 3.9 as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories with proper permissions
RUN mkdir -p uploads original_audio noisy_audio denoised_audio assets models templates \
    && chmod 777 uploads original_audio noisy_audio denoised_audio

# Copy the entire repository
COPY . .

# Ensure proper permissions for copied files
RUN chmod -R 755 /app

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Expose the port the app runs on
EXPOSE 6767

# Command to run the application
CMD ["python", "app.py"]