#! /bin/bash

#start the docker
docker exec -it ros-dist-ui bash

cd ~/Downloads/TormachZA6CNC/rosNodes/

#install necessary python packages
pip install ik-geo
pip install scipy

#source the custom ROS
source devel/setup.bash

#run the tormach controller 
rosrun tormach_controller controller.py



