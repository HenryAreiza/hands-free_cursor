# Create the docker image
docker build -t camera-app -f Dockerfile .
# Run the docker container
docker run --rm -it --device=/dev/video0 -v /media/dvd/DATA/repos/hands-free_cursor/docker_test/files/out:/app/files/out camera-app

##################################################
# Where the latest command computes the following:
#=> docker run: This is the command to start a new Docker container.
#=> --rm: This option tells Docker to automatically remove the container once it exits. This helps clean up containers after they are no longer needed, preventing them from accumulating on your system.
#=> -it: These options are used to run the container in interactive mode with a terminal attached. This allows you to interact with the container's command line.
#=> --device=/dev/video0: This option grants access to the /dev/video0 device inside the container. In this context, /dev/video0 typically represents the first video device, which is often the built-in webcam on a laptop or an externally connected camera. By using this option, the container can access and use the specified camera device for tasks such as image or video capture.
#=> -v /media/dvd/DATA/repos/hands-free_cursor/docker_test/files/out:/app/files/out: This option specifies a volume mount. It links a directory from your host system (/media/dvd/DATA/repos/hands-free_cursor/docker_test/files/out) to a directory within the container (/app/files/out). This means that any data written to the /app/files/out directory inside the container will be saved in the specified host directory on your computer. In the context of your previous project, this is where the captured images from the camera will be saved.
#=> camera-app: This is the name or tag of the Docker image that you want to run as a container. In your case, camera-app is the name of the Docker image you built from your Dockerfile, which contains the Python script for capturing camera images.