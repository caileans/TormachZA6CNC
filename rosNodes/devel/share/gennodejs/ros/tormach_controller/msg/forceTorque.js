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

class forceTorque {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.forcex = null;
      this.forcey = null;
      this.forcez = null;
      this.momenti = null;
      this.momentj = null;
      this.momentk = null;
    }
    else {
      if (initObj.hasOwnProperty('forcex')) {
        this.forcex = initObj.forcex
      }
      else {
        this.forcex = 0.0;
      }
      if (initObj.hasOwnProperty('forcey')) {
        this.forcey = initObj.forcey
      }
      else {
        this.forcey = 0.0;
      }
      if (initObj.hasOwnProperty('forcez')) {
        this.forcez = initObj.forcez
      }
      else {
        this.forcez = 0.0;
      }
      if (initObj.hasOwnProperty('momenti')) {
        this.momenti = initObj.momenti
      }
      else {
        this.momenti = 0.0;
      }
      if (initObj.hasOwnProperty('momentj')) {
        this.momentj = initObj.momentj
      }
      else {
        this.momentj = 0.0;
      }
      if (initObj.hasOwnProperty('momentk')) {
        this.momentk = initObj.momentk
      }
      else {
        this.momentk = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type forceTorque
    // Serialize message field [forcex]
    bufferOffset = _serializer.float32(obj.forcex, buffer, bufferOffset);
    // Serialize message field [forcey]
    bufferOffset = _serializer.float32(obj.forcey, buffer, bufferOffset);
    // Serialize message field [forcez]
    bufferOffset = _serializer.float32(obj.forcez, buffer, bufferOffset);
    // Serialize message field [momenti]
    bufferOffset = _serializer.float32(obj.momenti, buffer, bufferOffset);
    // Serialize message field [momentj]
    bufferOffset = _serializer.float32(obj.momentj, buffer, bufferOffset);
    // Serialize message field [momentk]
    bufferOffset = _serializer.float32(obj.momentk, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type forceTorque
    let len;
    let data = new forceTorque(null);
    // Deserialize message field [forcex]
    data.forcex = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [forcey]
    data.forcey = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [forcez]
    data.forcez = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [momenti]
    data.momenti = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [momentj]
    data.momentj = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [momentk]
    data.momentk = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 24;
  }

  static datatype() {
    // Returns string type for a message object
    return 'tormach_controller/forceTorque';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'b67716f2ec7095782e343db5f3543a2e';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 forcex
    float32 forcey
    float32 forcez
    float32 momenti
    float32 momentj
    float32 momentk
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new forceTorque(null);
    if (msg.forcex !== undefined) {
      resolved.forcex = msg.forcex;
    }
    else {
      resolved.forcex = 0.0
    }

    if (msg.forcey !== undefined) {
      resolved.forcey = msg.forcey;
    }
    else {
      resolved.forcey = 0.0
    }

    if (msg.forcez !== undefined) {
      resolved.forcez = msg.forcez;
    }
    else {
      resolved.forcez = 0.0
    }

    if (msg.momenti !== undefined) {
      resolved.momenti = msg.momenti;
    }
    else {
      resolved.momenti = 0.0
    }

    if (msg.momentj !== undefined) {
      resolved.momentj = msg.momentj;
    }
    else {
      resolved.momentj = 0.0
    }

    if (msg.momentk !== undefined) {
      resolved.momentk = msg.momentk;
    }
    else {
      resolved.momentk = 0.0
    }

    return resolved;
    }
};

module.exports = forceTorque;
