# Use a base image with Python
FROM python:latest

RUN apt-get update && apt-get install -y
RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y

# Set the working directory
WORKDIR /app

RUN pip install --upgrade pip

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install -r requirements.txt

# Create a directory for output files
RUN mkdir -p /app/files/out

# Copy the Python script into the container
COPY SaveAudio.py .

# Command to run the script
CMD ["python", "SaveAudio.py"]

