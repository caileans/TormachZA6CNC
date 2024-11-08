
(cl:in-package :asdf)

(defsystem "tormach_controller-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :actionlib_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "MovePoseAction" :depends-on ("_package_MovePoseAction"))
    (:file "_package_MovePoseAction" :depends-on ("_package"))
    (:file "MovePoseActionFeedback" :depends-on ("_package_MovePoseActionFeedback"))
    (:file "_package_MovePoseActionFeedback" :depends-on ("_package"))
    (:file "MovePoseActionGoal" :depends-on ("_package_MovePoseActionGoal"))
    (:file "_package_MovePoseActionGoal" :depends-on ("_package"))
    (:file "MovePoseActionResult" :depends-on ("_package_MovePoseActionResult"))
    (:file "_package_MovePoseActionResult" :depends-on ("_package"))
    (:file "MovePoseFeedback" :depends-on ("_package_MovePoseFeedback"))
    (:file "_package_MovePoseFeedback" :depends-on ("_package"))
    (:file "MovePoseGoal" :depends-on ("_package_MovePoseGoal"))
    (:file "_package_MovePoseGoal" :depends-on ("_package"))
    (:file "MovePoseResult" :depends-on ("_package_MovePoseResult"))
    (:file "_package_MovePoseResult" :depends-on ("_package"))
    (:file "forceTorque" :depends-on ("_package_forceTorque"))
    (:file "_package_forceTorque" :depends-on ("_package"))
    (:file "pose" :depends-on ("_package_pose"))
    (:file "_package_pose" :depends-on ("_package"))
  ))