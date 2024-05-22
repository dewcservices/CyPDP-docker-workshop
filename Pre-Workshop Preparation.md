# CyPDP Docker Workshop May 2024

## Pre-Workshop Preparation

This workshop is expected to be run in an Ubuntu VM. Run the following commands in a Terminal to prepare your environment:
- sudo apt update
- sudo apt upgrade
- sudo apt install vim git
- killall snap-store
- sudo snap refresh
- mkdir /home/$USER/my-dev
- mkdir /home/$USER/my-dev/dewc-docker-workshop

If you are running a VMWare Workstation you may also want to run the following command so that you can copy and paste from inside and outside the VM (you will need to restart the VM before this will start working):
- sudo apt install open-vm-tools-desktop

Install Docker and docker compose. Run the following commands in a Terminal:
- for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
- sudo apt-get update
- sudo apt-get install ca-certificates curl open-vm-tools open-vm-tools-desktop
- sudo install -m 0755 -d /etc/apt/keyrings
- sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
- sudo chmod a+r /etc/apt/keyrings/docker.asc
- echo "deb [arch=\$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
- sudo apt-get update
- sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
- sudo usermod -aG docker $USER
- sudo service docker start

and then restart the VM.

Ensure Docker and docker compose are installed, running and can be accessed without sudo. Run the following commands in a Terminal:
- docker version
- docker compose version

If you are using VSCode (recommended), the Docker extension will be very useful.

Open you IDE to the newly created directory dewc-docker-workshop.
