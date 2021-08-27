# Dry eye Checker

Measure the number of blinks and notify to prevent dry eye.



<br>


## Description
An increasing number of people are suffering from dry eye due to long hours of PC work.

As of 2018, 340 million people worldwide are said to have dry eye.

If there is little blinking (~ 10 times / minute), there is a risk of dry eye, and if there is a lot of blinking (40 ~ times / minute), there is already a possibility of dry eye.

In this project, Jetson nano will be used to measure the number of blinks per minute and notify of danger.

<br>


## Demo
(movie)

<br>


## Requirement
- Jetson Nano 2GB
    - OS:JetPack 4.5.1
- web camera(I used Logicool C270)

<br>

## Install
1.Clone this repository.

    $ git clone ...(this repository)
2.Allow display connection from container to host

    $ xhost +

3.Run docker container

    $ bash docker_blink_run.sh

- If the .sh file cannot be executed, execute the following.

        $ chmod +x docker_blink_run.sh

4.Setup in a container

    $ cd shared_data
    $ bash setup.sh


<br>

## Usage
After *Install* in container,

    $ python3 blink_measurement.py


<br>
