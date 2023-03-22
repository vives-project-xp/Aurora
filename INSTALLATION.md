Use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to install Raspberry pi os on a raspberry pi

Select Raspberry PI OS

![RaspberryPiOs](./Documenten/Raspberry%20pi/installation1.png)

Choose your destination location.
Select the gear icon in the right bottom corner.
Change hostname to **aurora**.local

![aurora.local](./Documenten/Raspberry%20pi/installation2.png)

Choose your **username** and **password**.

![username/password](./Documenten/Raspberry%20pi/installation3.png)

Setup your wifi credentials.

![username/password](./Documenten/Raspberry%20pi/installation4.png)

Save your settings and start the installation.
Once the installation is finished.
Insert the sd-card into the Pi and boot it up.

Once booted up. Login using [SSH](https://tutorials-raspberrypi.com/raspberry-pi-remote-access-by-using-ssh-and-putty/). The hostname should be **aurora.local* and use your username and password.

Run the following commands:
```
sudo apt-get update
sudo apt-get upgrade
sudo reboot
```

### Install git:
```
sudo apt install git
git config --global user.name "Your Name"
git config --global user.email "youremail@yourdomain.com"
```

Once you have git installed, you can clone our project to the Raspberry Pi.
```
git clone https://github.com/vives-project-xp/Aurora.git
```

### Install Docker:
```
curl -fsSL https://get.docker.com -o get-docker.sh sh get-docker.sh
```

Once docker is installed, you can start our project.
```
docker compose up -d --build
```

If everything works as it should, you can search for [aurora.local](http://aurora.local/)