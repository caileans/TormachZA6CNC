;; Auto-generated. Do not edit!


(when (boundp 'tormach_controller::MovePoseGoal)
  (if (not (find-package "TORMACH_CONTROLLER"))
    (make-package "TORMACH_CONTROLLER"))
  (shadow 'MovePoseGoal (find-package "TORMACH_CONTROLLER")))
(unless (find-package "TORMACH_CONTROLLER::MOVEPOSEGOAL")
  (make-package "TORMACH_CONTROLLER::MOVEPOSEGOAL"))

(in-package "ROS")
;;//! \htmlinclude MovePoseGoal.msg.html


(defclass tormach_controller::MovePoseGoal
  :super ros::object
  :slots (_goalx _goaly _goalz _goali _goalj _goalk _vel _postol _forcetol ))

(defmethod tormach_controller::MovePoseGoal
  (:init
   (&key
    ((:goalx __goalx) 0.0)
    ((:goaly __goaly) 0.0)
    ((:goalz __goalz) 0.0)
    ((:goali __goali) 0.0)
    ((:goalj __goalj) 0.0)
    ((:goalk __goalk) 0.0)
    ((:vel __vel) 0.0)
    ((:postol __postol) 0.0)
    ((:forcetol __forcetol) 0.0)
    )
   (send-super :init)
   (setq _goalx (float __goalx))
   (setq _goaly (float __goaly))
   (setq _goalz (float __goalz))
   (setq _goali (float __goali))
   (setq _goalj (float __goalj))
   (setq _goalk (float __goalk))
   (setq _vel (float __vel))
   (setq _postol (float __postol))
   (setq _forcetol (float __forcetol))
   self)
  (:goalx
   (&optional __goalx)
   (if __goalx (setq _goalx __goalx)) _goalx)
  (:goaly
   (&optional __goaly)
   (if __goaly (setq _goaly __goaly)) _goaly)
  (:goalz
   (&optional __goalz)
   (if __goalz (setq _goalz __goalz)) _goalz)
  (:goali
   (&optional __goali)
   (if __goali (setq _goali __goali)) _goali)
  (:goalj
   (&optional __goalj)
   (if __goalj (setq _goalj __goalj)) _goalj)
  (:goalk
   (&optional __goalk)
   (if __goalk (setq _goalk __goalk)) _goalk)
  (:vel
   (&optional __vel)
   (if __vel (setq _vel __vel)) _vel)
  (:postol
   (&optional __postol)
   (if __postol (setq _postol __postol)) _postol)
  (:forcetol
   (&optional __forcetol)
   (if __forcetol (setq _forcetol __forcetol)) _forcetol)
  (:serialization-length
   ()
   (+
    ;; float32 _goalx
    4
    ;; float32 _goaly
    4
    ;; float32 _goalz
    4
    ;; float32 _goali
    4
    ;; float32 _goalj
    4
    ;; float32 _goalk
    4
    ;; float32 _vel
    4
    ;; float32 _postol
    4
    ;; float32 _forcetol
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _goalx
       (sys::poke _goalx (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _goaly
       (sys::poke _goaly (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _goalz
       (sys::poke _goalz (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _goali
       (sys::poke _goali (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _goalj
       (sys::poke _goalj (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _goalk
       (sys::poke _goalk (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _vel
       (sys::poke _vel (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _postol
       (sys::poke _postol (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _forcetol
       (sys::poke _forcetol (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _goalx
     (setq _goalx (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _goaly
     (setq _goaly (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _goalz
     (setq _goalz (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _goali
     (setq _goali (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _goalj
     (setq _goalj (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _goalk
     (setq _goalk (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _vel
     (setq _vel (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _postol
     (setq _postol (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _forcetol
     (setq _forcetol (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get tormach_controller::MovePoseGoal :md5sum-) "9782a91330f66069042af5b1d4f2166d")
(setf (get tormach_controller::MovePoseGoal :datatype-) "tormach_controller/MovePoseGoal")
(setf (get tormach_controller::MovePoseGoal :definition-)
      "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======
float32 goalx
float32 goaly
float32 goalz
float32 goali
float32 goalj
float32 goalk
float32 vel
float32 postol
float32 forcetol

")



(provide :tormach_controller/MovePoseGoal "9782a91330f66069042af5b1d4f2166d")

