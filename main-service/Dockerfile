# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the app's files into the container
COPY server.py requirements.txt /app/
COPY templates/ /app/templates/
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the main service
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "server.py"]