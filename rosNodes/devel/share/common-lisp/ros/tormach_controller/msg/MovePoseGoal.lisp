; Auto-generated. Do not edit!


(cl:in-package tormach_controller-msg)


;//! \htmlinclude MovePoseGoal.msg.html

(cl:defclass <MovePoseGoal> (roslisp-msg-protocol:ros-message)
  ((goalx
    :reader goalx
    :initarg :goalx
    :type cl:float
    :initform 0.0)
   (goaly
    :reader goaly
    :initarg :goaly
    :type cl:float
    :initform 0.0)
   (goalz
    :reader goalz
    :initarg :goalz
    :type cl:float
    :initform 0.0)
   (goali
    :reader goali
    :initarg :goali
    :type cl:float
    :initform 0.0)
   (goalj
    :reader goalj
    :initarg :goalj
    :type cl:float
    :initform 0.0)
   (goalk
    :reader goalk
    :initarg :goalk
    :type cl:float
    :initform 0.0)
   (vel
    :reader vel
    :initarg :vel
    :type cl:float
    :initform 0.0)
   (postol
    :reader postol
    :initarg :postol
    :type cl:float
    :initform 0.0)
   (forcetol
    :reader forcetol
    :initarg :forcetol
    :type cl:float
    :initform 0.0))
)

(cl:defclass MovePoseGoal (<MovePoseGoal>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MovePoseGoal>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MovePoseGoal)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name tormach_controller-msg:<MovePoseGoal> is deprecated: use tormach_controller-msg:MovePoseGoal instead.")))

(cl:ensure-generic-function 'goalx-val :lambda-list '(m))
(cl:defmethod goalx-val ((m <MovePoseGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tormach_controller-msg:goalx-val is deprecated.  Use tormach_controller-msg:goalx instead.")
  (goalx m))

(cl:ensure-generic-function 'goaly-val :lambda-list '(m))
(cl:defmethod goaly-val ((m <MovePoseGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tormach_controller-msg:goaly-val is deprecated.  Use tormach_controller-msg:goaly instead.")
  (goaly m))

(cl:ensure-generic-function 'goalz-val :lambda-list '(m))
(cl:defmethod goalz-val ((m <MovePoseGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tormach_controller-msg:goalz-val is deprecated.  Use tormach_controller-msg:goalz instead.")
  (goalz m))

(cl:ensure-generic-function 'goali-val :lambda-list '(m))
(cl:defmethod goali-val ((m <MovePoseGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tormach_controller-msg:goali-val is deprecated.  Use tormach_controller-msg:goali instead.")
  (goali m))

(cl:ensure-generic-function 'goalj-val :lambda-list '(m))
(cl:defmethod goalj-val ((m <MovePoseGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tormach_controller-msg:goalj-val is deprecated.  Use tormach_controller-msg:goalj instead.")
  (goalj m))

(cl:ensure-generic-function 'goalk-val :lambda-list '(m))
(cl:defmethod goalk-val ((m <MovePoseGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tormach_controller-msg:goalk-val is deprecated.  Use tormach_controller-msg:goalk instead.")
  (goalk m))

(cl:ensure-generic-function 'vel-val :lambda-list '(m))
(cl:defmethod vel-val ((m <MovePoseGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tormach_controller-msg:vel-val is deprecated.  Use tormach_controller-msg:vel instead.")
  (vel m))

(cl:ensure-generic-function 'postol-val :lambda-list '(m))
(cl:defmethod postol-val ((m <MovePoseGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tormach_controller-msg:postol-val is deprecated.  Use tormach_controller-msg:postol instead.")
  (postol m))

(cl:ensure-generic-function 'forcetol-val :lambda-list '(m))
(cl:defmethod forcetol-val ((m <MovePoseGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tormach_controller-msg:forcetol-val is deprecated.  Use tormach_controller-msg:forcetol instead.")
  (forcetol m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MovePoseGoal>) ostream)
  "Serializes a message object of type '<MovePoseGoal>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'goalx))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'goaly))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'goalz))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'goali))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'goalj))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'goalk))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'vel))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'postol))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'forcetol))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MovePoseGoal>) istream)
  "Deserializes a message object of type '<MovePoseGoal>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'goalx) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'goaly) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'goalz) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'goali) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'goalj) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'goalk) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'vel) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'postol) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'forcetol) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MovePoseGoal>)))
  "Returns string type for a message object of type '<MovePoseGoal>"
  "tormach_controller/MovePoseGoal")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MovePoseGoal)))
  "Returns string type for a message object of type 'MovePoseGoal"
  "tormach_controller/MovePoseGoal")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MovePoseGoal>)))
  "Returns md5sum for a message object of type '<MovePoseGoal>"
  "9782a91330f66069042af5b1d4f2166d")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MovePoseGoal)))
  "Returns md5sum for a message object of type 'MovePoseGoal"
  "9782a91330f66069042af5b1d4f2166d")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MovePoseGoal>)))
  "Returns full string definition for message of type '<MovePoseGoal>"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%float32 goalx~%float32 goaly~%float32 goalz~%float32 goali~%float32 goalj~%float32 goalk~%float32 vel~%float32 postol~%float32 forcetol~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MovePoseGoal)))
  "Returns full string definition for message of type 'MovePoseGoal"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%float32 goalx~%float32 goaly~%float32 goalz~%float32 goali~%float32 goalj~%float32 goalk~%float32 vel~%float32 postol~%float32 forcetol~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MovePoseGoal>))
  (cl:+ 0
     4
     4
     4
     4
     4
     4
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MovePoseGoal>))
  "Converts a ROS message object to a list"
  (cl:list 'MovePoseGoal
    (cl:cons ':goalx (goalx msg))
    (cl:cons ':goaly (goaly msg))
    (cl:cons ':goalz (goalz msg))
    (cl:cons ':goali (goali msg))
    (cl:cons ':goalj (goalj msg))
    (cl:cons ':goalk (goalk msg))
    (cl:cons ':vel (vel msg))
    (cl:cons ':postol (postol msg))
    (cl:cons ':forcetol (forcetol msg))
))
