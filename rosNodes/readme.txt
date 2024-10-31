to run the ros node:

go to /src/tormach_controller/scripts/ and ensure that you have execution access for the buffer_node.py file (chmod +x buffer_node.py)

return to /rosNodes and build the project (catkin_make)

source the project (./devel/setup.bash)

then use the command rosrun tormach_controller buffer_node.py

