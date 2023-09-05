# Use a base image with Python and OpenCV
FROM python:latest

RUN apt-get update && apt-get install -y

# Set the working directory
WORKDIR /app

RUN pip install --upgrade pip

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install -r requirements.txt

# Create a directory for output images
RUN mkdir -p /app/files/out

# Copy the Python script into the container
COPY SaveImage.py .

# Command to run the script
CMD ["python", "SaveImage.py"]
