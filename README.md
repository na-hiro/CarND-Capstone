# udacity-carnd-capstone
This is the project repo for the final project of the Udacity Self-Driving Car Nanodegree: Programming a Real Self-Driving Car.

[//]: # (Image References)

[image1]: ./imgs/img1.png "img1"
[image2]: ./imgs/img2.png "img2"
[image3]: ./imgs/img3.png "img3"
[image4]: ./imgs/img4.png "img4"
[image5]: ./imgs/img5.png "img5"


# System Architecture
The following is a system architecture diagram showing the ROS nodes and topics used in the project.
![architecture](https://d17h27t6h515a5.cloudfront.net/topher/2017/September/59b6d115_final-project-ros-graph-v2/final-project-ros-graph-v2.png)

# Team BR menbers
Our team(BR) has four members.

Team member name | Udacity account email | Location
---------------- | --------------------- | --------
Hironori Nagai - Team Lead| hinagai.5963@gmail.com | Japan
Raphaell Maciel de Sousa   | raphaellmsousa@gmail.com | Brazil
Guilherme Bortolaso | gui.bortolaso@gmail.com | Brazil  
James Lee | kcbighuge@gmail.com | USA

## Traffic Light Detection
The Traffic light will be detected by a relatively compact ssd_mobilenet_v1_coco_2017_11_17 at high speed.
The class ID of the traffic light of this model is 10. After detecting the traffic light, classify the color of the traffic light. A classifier using CNN and FCN was applied. Good results were obtained in Simulator and Real World Testing.

## Waypoint Updater
This node realize to update the target speed characteristic of each waypoint based on traffic signal and obstacle detection data.

## DBW (Drive-By-Wire) Node
This node finally calculates throttle, brake, steering angle.

## Results
The running scene of the car in the simulator and the signal detection result in the real world are shown below.

![alt text][image1]

![alt text][image2]

![alt text][image3]

![alt text][image4]

![alt text][image5]


### Udacity Information
This is the project repo for the final project of the Udacity Self-Driving Car Nanodegree: Programming a Real Self-Driving Car. For more information about the project, see the project introduction [here](https://classroom.udacity.com/nanodegrees/nd013/parts/6047fe34-d93c-4f50-8336-b70ef10cb4b2/modules/e1a23b06-329a-4684-a717-ad476f0d8dff/lessons/462c933d-9f24-42d3-8bdc-a08a5fc866e4/concepts/5ab4b122-83e6-436d-850f-9f4d26627fd9).

Please use **one** of the two installation options, either native **or** docker installation.

### Native Installation

* Be sure that your workstation is running Ubuntu 16.04 Xenial Xerus or Ubuntu 14.04 Trusty Tahir. [Ubuntu downloads can be found here](https://www.ubuntu.com/download/desktop).
* If using a Virtual Machine to install Ubuntu, use the following configuration as minimum:
  * 2 CPU
  * 2 GB system memory
  * 25 GB of free hard drive space

  The Udacity provided virtual machine has ROS and Dataspeed DBW already installed, so you can skip the next two steps if you are using this.

* Follow these instructions to install ROS
  * [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu) if you have Ubuntu 16.04.
  * [ROS Indigo](http://wiki.ros.org/indigo/Installation/Ubuntu) if you have Ubuntu 14.04.
* [Dataspeed DBW](https://bitbucket.org/DataspeedInc/dbw_mkz_ros)
  * Use this option to install the SDK on a workstation that already has ROS installed: [One Line SDK Install (binary)](https://bitbucket.org/DataspeedInc/dbw_mkz_ros/src/81e63fcc335d7b64139d7482017d6a97b405e250/ROS_SETUP.md?fileviewer=file-view-default)
* Download the [Udacity Simulator](https://github.com/udacity/CarND-Capstone/releases).

### Docker Installation
[Install Docker](https://docs.docker.com/engine/installation/)

Build the docker container
```bash
docker build . -t capstone
```

Run the docker file
```bash
docker run -p 4567:4567 -v $PWD:/capstone -v /tmp/log:/root/.ros/ --rm -it capstone
```

### Port Forwarding
To set up port forwarding, please refer to the [instructions from term 2](https://classroom.udacity.com/nanodegrees/nd013/parts/40f38239-66b6-46ec-ae68-03afd8a601c8/modules/0949fca6-b379-42af-a919-ee50aa304e6a/lessons/f758c44c-5e40-4e01-93b5-1a82aa4e044f/concepts/16cf4a78-4fc7-49e1-8621-3450ca938b77)

### Usage

1. Clone the project repository
```bash
git clone https://github.com/udacity/CarND-Capstone.git
```

2. Install python dependencies
```bash
cd CarND-Capstone
pip install -r requirements.txt
```
3. Make and run styx
```bash
cd ros
catkin_make
source devel/setup.sh
roslaunch launch/styx.launch
```
4. Run the simulator

### Real world testing
1. Download [training bag](https://s3-us-west-1.amazonaws.com/udacity-selfdrivingcar/traffic_light_bag_file.zip) that was recorded on the Udacity self-driving car.
2. Unzip the file
```bash
unzip traffic_light_bag_file.zip
```
3. Play the bag file
```bash
rosbag play -l traffic_light_bag_file/traffic_light_training.bag
```
4. Launch your project in site mode
```bash
cd CarND-Capstone/ros
roslaunch launch/site.launch
```
5. Confirm that traffic light detection works on real life images
