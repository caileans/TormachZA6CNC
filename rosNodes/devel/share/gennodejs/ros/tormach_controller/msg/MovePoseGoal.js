// Auto-generated. Do not edit!

// (in-package tormach_controller.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class MovePoseGoal {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.goalx = null;
      this.goaly = null;
      this.goalz = null;
      this.goali = null;
      this.goalj = null;
      this.goalk = null;
      this.vel = null;
      this.postol = null;
      this.forcetol = null;
    }
    else {
      if (initObj.hasOwnProperty('goalx')) {
        this.goalx = initObj.goalx
      }
      else {
        this.goalx = 0.0;
      }
      if (initObj.hasOwnProperty('goaly')) {
        this.goaly = initObj.goaly
      }
      else {
        this.goaly = 0.0;
      }
      if (initObj.hasOwnProperty('goalz')) {
        this.goalz = initObj.goalz
      }
      else {
        this.goalz = 0.0;
      }
      if (initObj.hasOwnProperty('goali')) {
        this.goali = initObj.goali
      }
      else {
        this.goali = 0.0;
      }
      if (initObj.hasOwnProperty('goalj')) {
        this.goalj = initObj.goalj
      }
      else {
        this.goalj = 0.0;
      }
      if (initObj.hasOwnProperty('goalk')) {
        this.goalk = initObj.goalk
      }
      else {
        this.goalk = 0.0;
      }
      if (initObj.hasOwnProperty('vel')) {
        this.vel = initObj.vel
      }
      else {
        this.vel = 0.0;
      }
      if (initObj.hasOwnProperty('postol')) {
        this.postol = initObj.postol
      }
      else {
        this.postol = 0.0;
      }
      if (initObj.hasOwnProperty('forcetol')) {
        this.forcetol = initObj.forcetol
      }
      else {
        this.forcetol = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type MovePoseGoal
    // Serialize message field [goalx]
    bufferOffset = _serializer.float32(obj.goalx, buffer, bufferOffset);
    // Serialize message field [goaly]
    bufferOffset = _serializer.float32(obj.goaly, buffer, bufferOffset);
    // Serialize message field [goalz]
    bufferOffset = _serializer.float32(obj.goalz, buffer, bufferOffset);
    // Serialize message field [goali]
    bufferOffset = _serializer.float32(obj.goali, buffer, bufferOffset);
    // Serialize message field [goalj]
    bufferOffset = _serializer.float32(obj.goalj, buffer, bufferOffset);
    // Serialize message field [goalk]
    bufferOffset = _serializer.float32(obj.goalk, buffer, bufferOffset);
    // Serialize message field [vel]
    bufferOffset = _serializer.float32(obj.vel, buffer, bufferOffset);
    // Serialize message field [postol]
    bufferOffset = _serializer.float32(obj.postol, buffer, bufferOffset);
    // Serialize message field [forcetol]
    bufferOffset = _serializer.float32(obj.forcetol, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type MovePoseGoal
    let len;
    let data = new MovePoseGoal(null);
    // Deserialize message field [goalx]
    data.goalx = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [goaly]
    data.goaly = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [goalz]
    data.goalz = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [goali]
    data.goali = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [goalj]
    data.goalj = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [goalk]
    data.goalk = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [vel]
    data.vel = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [postol]
    data.postol = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [forcetol]
    data.forcetol = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 36;
  }

  static datatype() {
    // Returns string type for a message object
    return 'tormach_controller/MovePoseGoal';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '9782a91330f66069042af5b1d4f2166d';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======
    float32 goalx
    float32 goaly
    float32 goalz
    float32 goali
    float32 goalj
    float32 goalk
    float32 vel
    float32 postol
    float32 forcetol
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new MovePoseGoal(null);
    if (msg.goalx !== undefined) {
      resolved.goalx = msg.goalx;
    }
    else {
      resolved.goalx = 0.0
    }

    if (msg.goaly !== undefined) {
      resolved.goaly = msg.goaly;
    }
    else {
      resolved.goaly = 0.0
    }

    if (msg.goalz !== undefined) {
      resolved.goalz = msg.goalz;
    }
    else {
      resolved.goalz = 0.0
    }

    if (msg.goali !== undefined) {
      resolved.goali = msg.goali;
    }
    else {
      resolved.goali = 0.0
    }

    if (msg.goalj !== undefined) {
      resolved.goalj = msg.goalj;
    }
    else {
      resolved.goalj = 0.0
    }

    if (msg.goalk !== undefined) {
      resolved.goalk = msg.goalk;
    }
    else {
      resolved.goalk = 0.0
    }

    if (msg.vel !== undefined) {
      resolved.vel = msg.vel;
    }
    else {
      resolved.vel = 0.0
    }

    if (msg.postol !== undefined) {
      resolved.postol = msg.postol;
    }
    else {
      resolved.postol = 0.0
    }

    if (msg.forcetol !== undefined) {
      resolved.forcetol = msg.forcetol;
    }
    else {
      resolved.forcetol = 0.0
    }

    return resolved;
    }
};

module.exports = MovePoseGoal;