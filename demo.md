# Scenario

The goal of this demo is to demonstrate the GPU capabilities of Docker, and how to use these capbilities through Nuvla.

Since Docker 19, GPU usage when running a container can be achieved using --gpus all - this flag allows Docker to pass the GPU devices to the container.
This capability is only available to Nvidia GPUS. While the Docker client is able to use the GPU flag, Docker Compose hasn't caught up yet. This means we can't
use a docker-compose command to pass the GPU. 

We'll deploy a Docker container through Nuvla. To be able to use the GPU, we need to specify to the run command with Docker-Compose.


# DIY: Step by step guide 

For this demo we used a Nvidia Jetson Nano, but you might run this application on a computer with a Nvidia GPU, the correct drivers, and CUDA libraries that need to be installed, as well as Docker. 

Also, you'll need a camera connected through USB to the selected device.

To be able to deploy the application we also need a Nuvla account.

# Setup

Follow the NuvlaBox setup to connect your device to Nuvla. 

# Docker-Compose with GPU

As described above, Docker-Compose has no command to use de GPU directly. 
To use it we need to specify the run command in our Docker-Compose file. It looks like this:

version: '3.0'
services:
    darknet:
        image: 'franciscomendonca/darknet:1.0',
        ports:
            - "5000:5000"
        

# Deployment

in Nuvla.io, go to the App Store and find the app called "GPU Demo”. Click “launch”
A panel with appear - select your NuvlaBox credential from there

click on the environment tab and paste the “mqtt” URL that you saved above

env-var
