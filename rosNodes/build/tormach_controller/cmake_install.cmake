# Install script for directory: /home/yahboom/tormach/TormachZA6CNC/rosNodes/src/tormach_controller

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/yahboom/tormach/TormachZA6CNC/rosNodes/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tormach_controller/msg" TYPE FILE FILES
    "/home/yahboom/tormach/TormachZA6CNC/rosNodes/src/tormach_controller/msg/pose.msg"
    "/home/yahboom/tormach/TormachZA6CNC/rosNodes/src/tormach_controller/msg/forceTorque.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tormach_controller/action" TYPE FILE FILES "/home/yahboom/tormach/TormachZA6CNC/rosNodes/src/tormach_controller/action/MovePose.action")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tormach_controller/msg" TYPE FILE FILES
    "/home/yahboom/tormach/TormachZA6CNC/rosNodes/devel/share/tormach_controller/msg/MovePoseAction.msg"
    "/home/yahboom/tormach/TormachZA6CNC/rosNodes/devel/share/tormach_controller/msg/MovePoseActionGoal.msg"
    "/home/yahboom/tormach/TormachZA6CNC/rosNodes/devel/share/tormach_controller/msg/MovePoseActionResult.msg"
    "/home/yahboom/tormach/TormachZA6CNC/rosNodes/devel/share/tormach_controller/msg/MovePoseActionFeedback.msg"
    "/home/yahboom/tormach/TormachZA6CNC/rosNodes/devel/share/tormach_controller/msg/MovePoseGoal.msg"
    "/home/yahboom/tormach/TormachZA6CNC/rosNodes/devel/share/tormach_controller/msg/MovePoseResult.msg"
    "/home/yahboom/tormach/TormachZA6CNC/rosNodes/devel/share/tormach_controller/msg/MovePoseFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tormach_controller/cmake" TYPE FILE FILES "/home/yahboom/tormach/TormachZA6CNC/rosNodes/build/tormach_controller/catkin_generated/installspace/tormach_controller-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/yahboom/tormach/TormachZA6CNC/rosNodes/devel/include/tormach_controller")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/yahboom/tormach/TormachZA6CNC/rosNodes/devel/share/roseus/ros/tormach_controller")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/yahboom/tormach/TormachZA6CNC/rosNodes/devel/share/common-lisp/ros/tormach_controller")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/yahboom/tormach/TormachZA6CNC/rosNodes/devel/share/gennodejs/ros/tormach_controller")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/yahboom/tormach/TormachZA6CNC/rosNodes/devel/lib/python3/dist-packages/tormach_controller")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/yahboom/tormach/TormachZA6CNC/rosNodes/devel/lib/python3/dist-packages/tormach_controller")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/yahboom/tormach/TormachZA6CNC/rosNodes/build/tormach_controller/catkin_generated/installspace/tormach_controller.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tormach_controller/cmake" TYPE FILE FILES "/home/yahboom/tormach/TormachZA6CNC/rosNodes/build/tormach_controller/catkin_generated/installspace/tormach_controller-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tormach_controller/cmake" TYPE FILE FILES
    "/home/yahboom/tormach/TormachZA6CNC/rosNodes/build/tormach_controller/catkin_generated/installspace/tormach_controllerConfig.cmake"
    "/home/yahboom/tormach/TormachZA6CNC/rosNodes/build/tormach_controller/catkin_generated/installspace/tormach_controllerConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/tormach_controller" TYPE FILE FILES "/home/yahboom/tormach/TormachZA6CNC/rosNodes/src/tormach_controller/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/tormach_controller" TYPE PROGRAM FILES "/home/yahboom/tormach/TormachZA6CNC/rosNodes/build/tormach_controller/catkin_generated/installspace/buffer_node.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/tormach_controller" TYPE PROGRAM FILES "/home/yahboom/tormach/TormachZA6CNC/rosNodes/build/tormach_controller/catkin_generated/installspace/move_pose_action.py")
endif()
