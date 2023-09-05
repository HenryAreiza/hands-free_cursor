# Use a base image with Python
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

# Install package dependencies
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        alsa-base \
        alsa-utils \
        libsndfile1-dev && \
    apt-get clean

#RUN apt-get update && apt-get install -y
RUN apt-get install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y
RUN apt-get install -y alsa-base alsa-utils

# Set the working directory
WORKDIR /app

RUN apt install python3-pip -y
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
CMD ["/bin/bash"]
# CMD ["python3", "SaveAudio.py"]

