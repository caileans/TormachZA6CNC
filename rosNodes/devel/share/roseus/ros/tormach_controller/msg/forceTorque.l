;; Auto-generated. Do not edit!


(when (boundp 'tormach_controller::forceTorque)
  (if (not (find-package "TORMACH_CONTROLLER"))
    (make-package "TORMACH_CONTROLLER"))
  (shadow 'forceTorque (find-package "TORMACH_CONTROLLER")))
(unless (find-package "TORMACH_CONTROLLER::FORCETORQUE")
  (make-package "TORMACH_CONTROLLER::FORCETORQUE"))

(in-package "ROS")
;;//! \htmlinclude forceTorque.msg.html


(defclass tormach_controller::forceTorque
  :super ros::object
  :slots (_forcex _forcey _forcez _momenti _momentj _momentk ))

(defmethod tormach_controller::forceTorque
  (:init
   (&key
    ((:forcex __forcex) 0.0)
    ((:forcey __forcey) 0.0)
    ((:forcez __forcez) 0.0)
    ((:momenti __momenti) 0.0)
    ((:momentj __momentj) 0.0)
    ((:momentk __momentk) 0.0)
    )
   (send-super :init)
   (setq _forcex (float __forcex))
   (setq _forcey (float __forcey))
   (setq _forcez (float __forcez))
   (setq _momenti (float __momenti))
   (setq _momentj (float __momentj))
   (setq _momentk (float __momentk))
   self)
  (:forcex
   (&optional __forcex)
   (if __forcex (setq _forcex __forcex)) _forcex)
  (:forcey
   (&optional __forcey)
   (if __forcey (setq _forcey __forcey)) _forcey)
  (:forcez
   (&optional __forcez)
   (if __forcez (setq _forcez __forcez)) _forcez)
  (:momenti
   (&optional __momenti)
   (if __momenti (setq _momenti __momenti)) _momenti)
  (:momentj
   (&optional __momentj)
   (if __momentj (setq _momentj __momentj)) _momentj)
  (:momentk
   (&optional __momentk)
   (if __momentk (setq _momentk __momentk)) _momentk)
  (:serialization-length
   ()
   (+
    ;; float32 _forcex
    4
    ;; float32 _forcey
    4
    ;; float32 _forcez
    4
    ;; float32 _momenti
    4
    ;; float32 _momentj
    4
    ;; float32 _momentk
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _forcex
       (sys::poke _forcex (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _forcey
       (sys::poke _forcey (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _forcez
       (sys::poke _forcez (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _momenti
       (sys::poke _momenti (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _momentj
       (sys::poke _momentj (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _momentk
       (sys::poke _momentk (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _forcex
     (setq _forcex (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _forcey
     (setq _forcey (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _forcez
     (setq _forcez (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _momenti
     (setq _momenti (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _momentj
     (setq _momentj (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _momentk
     (setq _momentk (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get tormach_controller::forceTorque :md5sum-) "b67716f2ec7095782e343db5f3543a2e")
(setf (get tormach_controller::forceTorque :datatype-) "tormach_controller/forceTorque")
(setf (get tormach_controller::forceTorque :definition-)
      "float32 forcex
float32 forcey
float32 forcez
float32 momenti
float32 momentj
float32 momentk

")



(provide :tormach_controller/forceTorque "b67716f2ec7095782e343db5f3543a2e")


