; Auto-generated. Do not edit!


(cl:in-package tormach_controller-msg)


;//! \htmlinclude forceTorque.msg.html

(cl:defclass <forceTorque> (roslisp-msg-protocol:ros-message)
  ((forcex
    :reader forcex
    :initarg :forcex
    :type cl:float
    :initform 0.0)
   (forcey
    :reader forcey
    :initarg :forcey
    :type cl:float
    :initform 0.0)
   (forcez
    :reader forcez
    :initarg :forcez
    :type cl:float
    :initform 0.0)
   (momenti
    :reader momenti
    :initarg :momenti
    :type cl:float
    :initform 0.0)
   (momentj
    :reader momentj
    :initarg :momentj
    :type cl:float
    :initform 0.0)
   (momentk
    :reader momentk
    :initarg :momentk
    :type cl:float
    :initform 0.0))
)

(cl:defclass forceTorque (<forceTorque>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <forceTorque>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'forceTorque)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name tormach_controller-msg:<forceTorque> is deprecated: use tormach_controller-msg:forceTorque instead.")))

(cl:ensure-generic-function 'forcex-val :lambda-list '(m))
(cl:defmethod forcex-val ((m <forceTorque>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tormach_controller-msg:forcex-val is deprecated.  Use tormach_controller-msg:forcex instead.")
  (forcex m))

(cl:ensure-generic-function 'forcey-val :lambda-list '(m))
(cl:defmethod forcey-val ((m <forceTorque>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tormach_controller-msg:forcey-val is deprecated.  Use tormach_controller-msg:forcey instead.")
  (forcey m))

(cl:ensure-generic-function 'forcez-val :lambda-list '(m))
(cl:defmethod forcez-val ((m <forceTorque>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tormach_controller-msg:forcez-val is deprecated.  Use tormach_controller-msg:forcez instead.")
  (forcez m))

(cl:ensure-generic-function 'momenti-val :lambda-list '(m))
(cl:defmethod momenti-val ((m <forceTorque>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tormach_controller-msg:momenti-val is deprecated.  Use tormach_controller-msg:momenti instead.")
  (momenti m))

(cl:ensure-generic-function 'momentj-val :lambda-list '(m))
(cl:defmethod momentj-val ((m <forceTorque>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tormach_controller-msg:momentj-val is deprecated.  Use tormach_controller-msg:momentj instead.")
  (momentj m))

(cl:ensure-generic-function 'momentk-val :lambda-list '(m))
(cl:defmethod momentk-val ((m <forceTorque>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader tormach_controller-msg:momentk-val is deprecated.  Use tormach_controller-msg:momentk instead.")
  (momentk m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <forceTorque>) ostream)
  "Serializes a message object of type '<forceTorque>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'forcex))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'forcey))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'forcez))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'momenti))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'momentj))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'momentk))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <forceTorque>) istream)
  "Deserializes a message object of type '<forceTorque>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'forcex) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'forcey) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'forcez) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'momenti) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'momentj) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'momentk) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<forceTorque>)))
  "Returns string type for a message object of type '<forceTorque>"
  "tormach_controller/forceTorque")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'forceTorque)))
  "Returns string type for a message object of type 'forceTorque"
  "tormach_controller/forceTorque")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<forceTorque>)))
  "Returns md5sum for a message object of type '<forceTorque>"
  "b67716f2ec7095782e343db5f3543a2e")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'forceTorque)))
  "Returns md5sum for a message object of type 'forceTorque"
  "b67716f2ec7095782e343db5f3543a2e")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<forceTorque>)))
  "Returns full string definition for message of type '<forceTorque>"
  (cl:format cl:nil "float32 forcex~%float32 forcey~%float32 forcez~%float32 momenti~%float32 momentj~%float32 momentk~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'forceTorque)))
  "Returns full string definition for message of type 'forceTorque"
  (cl:format cl:nil "float32 forcex~%float32 forcey~%float32 forcez~%float32 momenti~%float32 momentj~%float32 momentk~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <forceTorque>))
  (cl:+ 0
     4
     4
     4
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <forceTorque>))
  "Converts a ROS message object to a list"
  (cl:list 'forceTorque
    (cl:cons ':forcex (forcex msg))
    (cl:cons ':forcey (forcey msg))
    (cl:cons ':forcez (forcez msg))
    (cl:cons ':momenti (momenti msg))
    (cl:cons ':momentj (momentj msg))
    (cl:cons ':momentk (momentk msg))
))
