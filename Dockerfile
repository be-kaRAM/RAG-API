# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Set PYTHONPATH
ENV PYTHONPATH=/app

# Expose the port the app runs on (8080)
EXPOSE 8080

# Set the command to run the application
CMD ["python", "-m", "app.main"]
