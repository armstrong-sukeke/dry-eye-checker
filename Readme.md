# Dry Eye Checker

Measure the number of blinks and notify to prevent dry eye.



<br>


## Description
An increasing number of people are suffering from dry eye due to long hours of PC work.

As of 2018, 340 million people worldwide are said to have dry eye.

If there is little blinking (~ 10 times / minute), there is a risk of dry eye, and if there is a lot of blinking (40 ~ times / minute), there is already a possibility of dry eye.

In this project, Jetson nano will be used to measure the number of blinks per minute and notify of danger.

![](https://github.com/armstrong-sukeke/dry-eye-checker/blob/main/image/dry-eye-description.png)

<br>


## Demo
[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/kQxYPSaJ-jE/0.jpg)](http://www.youtube.com/watch?v=kQxYPSaJ-jE)

https://www.youtube.com/watch?v=kQxYPSaJ-jE

<br>


## Requirement
- Jetson Nano 2GB
    - OS:JetPack 4.5.1
- web camera(I used Logicool C270)

<br>

## Install
1.Clone this repository.

    $ cd /home/nvidia
    $ git clone https://github.com/armstrong-sukeke/dry-eye-checker.git

2.Allow display connection from container to host

    $ xhost +

3.Run docker container

    $ cd dry-eye-checker
    $ bash docker_blink_run.sh

- If the .sh file cannot be executed, execute the following.

        $ chmod +x docker_blink_run.sh

4.Setup in the container(50min)

    $ cd shared_data
    $ bash setup.sh
    


<br>

## Usage
After *Install* in container,

    $ cd shared_data
    $ python3 blink_measurement.py

You can permanently measure blinks [times / min].

<br>
