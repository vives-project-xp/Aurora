# Aurora
our inspiration for this project is the northern lights in Norway. This we want to recreate using ledstrips,  also we will try to develop a person detection system

![ifJPbUm9XMsQdt7AQAets-1200-80](https://user-images.githubusercontent.com/83211667/222449053-1e7f0ad8-25d7-4f5e-bab7-4125bcd5382a.jpg)


## Table of contents

- Short discription
- Required
  - Hardware
  - Software
- Installation
- Configuration
- Troubleshooting
- FAQ
- Maintainers
- project photos

## Short Discription

The project for the ARGB led strip and motion sensor.
This is an interactive LED strip that tracks people 

## Required

These are the required software and hardware

 ### Software
 
 - Wled
 - Arduino
 - HTML
 - Python
 - Javascript
 
 ### Hardware

 - ESP32
 - WS2812B led strip
 - kabel goot 
 - 2,5 carre kabels
 - breadboard
 - Voeding
 - IR sensor
 - 3d printed brackets
  

## Installation

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

Once booted up. Login using SSH and your username and password.

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

If everything works as it should, you can search for [aurora.local](aurora.local)

## Configuration

No configuration yet

## Troubleshooting

No problems yet

## FAQ

no questions yet

## Maintainers
Made by  Glenn Coopman, Aitor Vannevel, thibaut schroyens, Thomas Oddery and Robbe Verhelst

## project photos

![image](https://user-images.githubusercontent.com/83211667/222438233-dfeb06dd-3df8-4e37-b3ea-25aaaac1e787.png)


### sfeerbeelden
![20230309_151527](https://user-images.githubusercontent.com/83211667/224052116-a657af65-2819-487f-a10e-55401445fedb.jpg)
