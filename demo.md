# Scenario

The goal of this demo is to demonstrate the GPU capabilities of Docker, and how to use these capbilities through Nuvla.

Since Docker 19, GPU usage when running a container can be achieved using --gpus all - this flag allows Docker to pass the GPU devices to the container.
This capability is only available to Nvidia GPUS. While the Docker client is able to use the GPU flag, Docker Compose hasn't caught up yet. This means we can't
use a docker-compose command to pass the GPU. 

We'll deploy a Docker container through Nuvla. To be able to use the GPU, we need to specify to the run command with Docker-Compose.


# DIY: Step by step guide 

For this demo we used a Nvidia Jetson Nano, 