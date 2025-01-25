import numpy as np
from dataclasses import dataclass

@dataclass
class JointState:
    time: np.array([])
    pos: np.array([])
    vel: np.array([])
    accel: np.array([])
    eff: np.array([])

def readJointStatesFile(fileName, data, initialTime):
    c=1
    # initialTime=0
    with open(fileName, 'r') as file:
        for line in file:
            # print(line.strip())
            temp=line.strip()
            if (c%19)==4: #secs
                temp=float(temp.split(':')[1].split(' ')[-1])
                # if c==4:
                #     initialTime=temp;			
                data.time=np.append(data.time,temp)
            elif (c%19)==5: #nsecs
                temp=float(temp.split(':')[1].split(' ')[-1])
                # if c==5:
                #     initialTime+=temp/10.0**9
                data.time[-1]+= temp/10.0**9 - initialTime
            elif (c%19)==16: #position
                temp=temp.split('[')[1][0:-1].split(',')
                data.pos=np.append(data.pos,[np.array(temp, dtype=float)], axis=0)
            elif (c%19)==17: #velocity
                temp=temp.split('[')[1][0:-1].split(',')
                data.vel=np.append(data.vel,[np.array(temp, dtype=float)], axis=0)
            elif(c%19)==18: #effort
                temp=temp.split('[')[1][0:-1].split(',')
                data.eff=np.append(data.eff,[np.array(temp, dtype=float)], axis=0)
            c+=1


def readJointCommandFile(fileName, data, initialTime):
    c=1
    # initialTime=0
    with open(fileName, 'r') as file:
        for line in file:
            # print(line.strip())
            temp=line.strip()
            if (c%25)==4: #secs
                temp=float(temp.split(':')[1].split(' ')[-1])
                # if c==4:
                #     initialTime=temp;			
                data.time=np.append(data.time,temp)
            elif (c%25)==5: #nsecs
                temp=float(temp.split(':')[1].split(' ')[-1])
                # if c==5:
                #     initialTime+=temp/10.0**9
                data.time[-1]+= temp/10.0**9 - initialTime
            elif (c%25)==18: #position
                temp=temp.split('[')[1][0:-1].split(',')
                data.pos=np.append(data.pos,[np.array(temp, dtype=float)], axis=0)
            # elif (c%25)==19: #velocity
            #     temp=temp.split('[')[1][0:-1].split(',')
            #     data.vel=np.append(data.vel,[np.array(temp, dtype=float)], axis=0)
            # elif (c%25)==20: #accel
            #     temp=temp.split('[')[1][0:-1].split(',')
            #     data.accel=np.append(data.accel,[np.array(temp, dtype=float)], axis=0)
            # elif(c%19)==21: #effort
            #     temp=temp.split('[')[1][0:-1].split(',')
            #     data.eff=np.append(data.eff,[np.array(temp, dtype=float)], axis=0)
            c+=1