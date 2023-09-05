# Create the docker image
docker build -f Dockerfile --no-cache --tag=audio:0.0.1 
# Run the docker container
docker run -it --rm --device /dev/snd -v /media/dvd/DATA/repos/hands-free_cursor/docker_test/files/out:/app/files/out audio:0.0.1
# Inside the docker you may have to specify your audio device and sampling rate, e.g.:
($container$): python3 --device 6 --sample_rate 32000


##################################################
#=> -it: These flags are used together and stand for "interactive" and "pseudo-TTY." They make the container run in interactive mode, allowing you to interact with the container's shell.
#=> --rm: This flag tells Docker to automatically remove the container when it exits. This is useful for temporary containers that you don't want to leave behind after they've completed their task.
#=> --device /dev/snd: This flag allows you to pass the /dev/snd device (sound device) from the host machine to the container. It's essential for the container to access and utilize the host's sound hardware.
#=> -v /media/dvd/DATA/repos/hands-free_cursor/docker_test/files/out:/app/files/out: This flag uses Docker's volume mounting feature. It maps a directory or file from the host machine (in this case, /media/dvd/DATA/repos/hands-free_cursor/docker_test/files/out) to a directory within the container (/app/files/out). This allows the container to read and write data to the specified directory on the host machine.
#=> audio:0.0.1: This is the name and tag of the Docker image that you want to run. It specifies the image to use for creating the container. In this case, the image is named "audio" with a version or tag "0.0.1."