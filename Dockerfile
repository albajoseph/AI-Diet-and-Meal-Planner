# Use Python 3.12 as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements and install dependencies
# (If you don't have a requirements.txt, we install manually here)
RUN pip install --no-cache-dir fastapi uvicorn requests python-dotenv

# Copy the rest of the application code
COPY . .

# Expose port 8000
EXPOSE 8000

# Command to run the application
# --host 0.0.0.0 is crucial for Docker to accept outside connections
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]