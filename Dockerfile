# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Make the setup_env.sh script executable
RUN chmod +x setup_env.sh

# Run the setup_env.sh script to prepare the environment
RUN ./setup_env.sh

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for communication (if needed)
EXPOSE 5000

# Set environment variables
ENV ENV=production

# Command to run the application with runtime arguments
ENTRYPOINT ["python", "src/main.py"]