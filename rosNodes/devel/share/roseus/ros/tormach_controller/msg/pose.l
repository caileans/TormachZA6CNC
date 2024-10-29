;; Auto-generated. Do not edit!


(when (boundp 'tormach_controller::pose)
  (if (not (find-package "TORMACH_CONTROLLER"))
    (make-package "TORMACH_CONTROLLER"))
  (shadow 'pose (find-package "TORMACH_CONTROLLER")))
(unless (find-package "TORMACH_CONTROLLER::POSE")
  (make-package "TORMACH_CONTROLLER::POSE"))

(in-package "ROS")
;;//! \htmlinclude pose.msg.html


(defclass tormach_controller::pose
  :super ros::object
  :slots (_x _y _z _i _j _k ))

(defmethod tormach_controller::pose
  (:init
   (&key
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    ((:z __z) 0.0)
    ((:i __i) 0.0)
    ((:j __j) 0.0)
    ((:k __k) 0.0)
    )
   (send-super :init)
   (setq _x (float __x))
   (setq _y (float __y))
   (setq _z (float __z))
   (setq _i (float __i))
   (setq _j (float __j))
   (setq _k (float __k))
   self)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:z
   (&optional __z)
   (if __z (setq _z __z)) _z)
  (:i
   (&optional __i)
   (if __i (setq _i __i)) _i)
  (:j
   (&optional __j)
   (if __j (setq _j __j)) _j)
  (:k
   (&optional __k)
   (if __k (setq _k __k)) _k)
  (:serialization-length
   ()
   (+
    ;; float32 _x
    4
    ;; float32 _y
    4
    ;; float32 _z
    4
    ;; float32 _i
    4
    ;; float32 _j
    4
    ;; float32 _k
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _x
       (sys::poke _x (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _y
       (sys::poke _y (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _z
       (sys::poke _z (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _i
       (sys::poke _i (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _j
       (sys::poke _j (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _k
       (sys::poke _k (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _x
     (setq _x (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _y
     (setq _y (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _z
     (setq _z (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _i
     (setq _i (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _j
     (setq _j (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _k
     (setq _k (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get tormach_controller::pose :md5sum-) "984c0c99d8fcaf28a3e4d0fe3ad549f2")
(setf (get tormach_controller::pose :datatype-) "tormach_controller/pose")
(setf (get tormach_controller::pose :definition-)
      "float32 x
float32 y
float32 z
float32 i
float32 j
float32 k

")



(provide :tormach_controller/pose "984c0c99d8fcaf28a3e4d0fe3ad549f2")


