# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file if you have one, otherwise manually install dependencies
COPY ./requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory to the container
COPY . /app

# Expose the port on which the app will run
EXPOSE 2000

# Run the FastAPI application using Uvicorn
CMD ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "2000"]
