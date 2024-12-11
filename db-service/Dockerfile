# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the app's files into the container
COPY db_service.py requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5001 for the database service
EXPOSE 5001

# Command to run the database service
CMD ["python", "db_service.py"]