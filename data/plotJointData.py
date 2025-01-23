import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class State:
    time: np.array([])
    pos: np.array([])
    vel: np.array([])

def readStatesFile(fileName, data, initialTime):
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
            # elif(c%19)==18:
            #     temp=temp.split('[')[1].split(',')
            #     eff=np.append(eff,[[float(temp[0]),float(temp[1])]], axis=0)
            c+=1


def readCommandFile(fileName, data, initialTime):
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
            # elif (c%25)==17: #velocity
            #     temp=temp.split('[')[1].split(',')
            #     vel=np.append(vel,[[float(temp[0]),float(temp[1])]], axis=0)
            # elif(c%19)==18:
            #     temp=temp.split('[')[1].split(',')
            #     eff=np.append(eff,[[float(temp[0]),float(temp[1])]], axis=0)
            c+=1


test1command = State([0.], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]])
test1states  = State([0.], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]])
test2command = State([0.], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]])
test2states  = State([0.], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]])
test3command = State([0.], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]])
test3states  = State([0.], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]])
test4command = State([0.], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]])
test4states  = State([0.], [[0.,0.,0.,0.,0.,0.,0.,0.]], [[0.,0.,0.,0.,0.,0.,0.,0.]])

test1InitTime = 1737602693.0
test2InitTime = 1737602888.0
test3InitTime = 1737603596.0
test4InitTime = 1737603821.0




readCommandFile('1_22_25_test1_command.txt', test1command, initialTime=test1InitTime)
readCommandFile('1_22_25_test2_command.txt', test2command, initialTime=test2InitTime)
readCommandFile('1_22_25_test3_command.txt', test3command, initialTime=test3InitTime)
readCommandFile('1_22_25_test4_command.txt', test4command, initialTime=test4InitTime)

readStatesFile('1_22_25_test1_states.txt', test1states, initialTime=test1InitTime)
readStatesFile('1_22_25_test2_states.txt', test2states, initialTime=test2InitTime)
readStatesFile('1_22_25_test3_states.txt', test3states, initialTime=test3InitTime)
readStatesFile('1_22_25_test4_states.txt', test4states, initialTime=test4InitTime)


            

plt.plot(test1command.time[1:], test1command.pos[1:, 0], 'k.')
plt.plot(test1states.time[1:],test1states.pos[1:,0],'b.')
plt.plot(test1states.time[1:],test1states.pos[1:,1],'g.')
plt.plot(test1states.time[1:],test1states.pos[1:,2],'r.')
plt.plot(test1states.time[1:],test1states.pos[1:,3],'c.')
plt.plot(test1states.time[1:],test1states.pos[1:,4],'m.')
plt.plot(test1states.time[1:],test1states.pos[1:,5],'y.')
plt.plot(test1states.time[1:],test1states.vel[1:,0],'b+')
plt.plot(test1states.time[1:],test1states.vel[1:,1],'g+')
plt.plot(test1states.time[1:],test1states.vel[1:,2],'r+')
plt.plot(test1states.time[1:],test1states.vel[1:,3],'c+')
plt.plot(test1states.time[1:],test1states.vel[1:,4],'m+')
plt.plot(test1states.time[1:],test1states.vel[1:,5],'y+')
# plt.axis((11.5,16.5,-.2,.3))
plt.ylabel('Joint Postition (rad) / Velocity (rad/s)')
plt.xlabel('Time (s)')
plt.legend(['Commanded pos', 'Joint 1 pos', 'Joint 2 pos', 'Joint 3 pos', 'Joint 4 pos', 'Joint 5 pos', 'Joint 6 pos', 'Joint 1 vel', 'Joint 2 vel', 'Joint 3 vel', 'Joint 4 vel', 'Joint 5 vel', 'Joint 6 vel'])
plt.title('Test 1: 8rad/sec2, 2rad/s, no overshoot')
plt.show()



plt.plot(test2command.time[1:], test1command.pos[1:, 0], 'k.')
plt.plot(test2states.time[1:],test2states.pos[1:,0],'b.')
plt.plot(test2states.time[1:],test2states.pos[1:,1],'g.')
plt.plot(test2states.time[1:],test2states.pos[1:,2],'r.')
plt.plot(test2states.time[1:],test2states.pos[1:,3],'c.')
plt.plot(test2states.time[1:],test2states.pos[1:,4],'m.')
plt.plot(test2states.time[1:],test2states.pos[1:,5],'y.')
plt.plot(test2states.time[1:],test2states.vel[1:,0],'b+')
plt.plot(test2states.time[1:],test2states.vel[1:,1],'g+')
plt.plot(test2states.time[1:],test2states.vel[1:,2],'r+')
plt.plot(test2states.time[1:],test2states.vel[1:,3],'c+')
plt.plot(test2states.time[1:],test2states.vel[1:,4],'m+')
plt.plot(test2states.time[1:],test2states.vel[1:,5],'y+')
# plt.axis((11.5,16.5,-.2,.3))
plt.ylabel('Joint Postition (rad) / Velocity (rad/s)')
plt.xlabel('Time (s)')
plt.legend(['Commanded pos', 'Joint 1 pos', 'Joint 2 pos', 'Joint 3 pos', 'Joint 4 pos', 'Joint 5 pos', 'Joint 6 pos', 'Joint 1 vel', 'Joint 2 vel', 'Joint 3 vel', 'Joint 4 vel', 'Joint 5 vel', 'Joint 6 vel'])
plt.title('Test 2: 8rad/sec2, 2rad/s, 2x overshoot')
plt.show()

plt.plot(test3command.time[1:], test3command.pos[1:, 0], 'k.')
plt.plot(test3states.time[1:],test3states.pos[1:,0],'b.')
plt.plot(test3states.time[1:],test3states.pos[1:,1],'g.')
plt.plot(test3states.time[1:],test3states.pos[1:,2],'r.')
plt.plot(test3states.time[1:],test3states.pos[1:,3],'c.')
plt.plot(test3states.time[1:],test3states.pos[1:,4],'m.')
plt.plot(test3states.time[1:],test3states.pos[1:,5],'y.')
plt.plot(test3states.time[1:],test3states.vel[1:,0],'b+')
plt.plot(test3states.time[1:],test3states.vel[1:,1],'g+')
plt.plot(test3states.time[1:],test3states.vel[1:,2],'r+')
plt.plot(test3states.time[1:],test3states.vel[1:,3],'c+')
plt.plot(test3states.time[1:],test3states.vel[1:,4],'m+')
plt.plot(test3states.time[1:],test3states.vel[1:,5],'y+')
# plt.axis((11.5,16.5,-.2,.3))
plt.ylabel('Joint Postition (rad) / Velocity (rad/s)')
plt.xlabel('Time (s)')
plt.legend(['Commanded pos', 'Joint 1 pos', 'Joint 2 pos', 'Joint 3 pos', 'Joint 4 pos', 'Joint 5 pos', 'Joint 6 pos', 'Joint 1 vel', 'Joint 2 vel', 'Joint 3 vel', 'Joint 4 vel', 'Joint 5 vel', 'Joint 6 vel'])
plt.title('Test 3: 0.3rad/sec2, 0.3rad/s, no overshoot')
plt.show()


plt.plot(test4command.time[1:], test3command.pos[1:, 0], 'k.')
plt.plot(test4states.time[1:],test4states.pos[1:,0],'b.')
plt.plot(test4states.time[1:],test4states.pos[1:,1],'g.')
plt.plot(test4states.time[1:],test4states.pos[1:,2],'r.')
plt.plot(test4states.time[1:],test4states.pos[1:,3],'c.')
plt.plot(test4states.time[1:],test4states.pos[1:,4],'m.')
plt.plot(test4states.time[1:],test4states.pos[1:,5],'y.')
plt.plot(test4states.time[1:],test4states.vel[1:,0],'b+')
plt.plot(test4states.time[1:],test4states.vel[1:,1],'g+')
plt.plot(test4states.time[1:],test4states.vel[1:,2],'r+')
plt.plot(test4states.time[1:],test4states.vel[1:,3],'c+')
plt.plot(test4states.time[1:],test4states.vel[1:,4],'m+')
plt.plot(test4states.time[1:],test4states.vel[1:,5],'y+')
# plt.axis((11.5,16.5,-.2,.3))
plt.ylabel('Joint Postition (rad) / Velocity (rad/s)')
plt.xlabel('Time (s)')
plt.legend(['Commanded pos', 'Joint 1 pos', 'Joint 2 pos', 'Joint 3 pos', 'Joint 4 pos', 'Joint 5 pos', 'Joint 6 pos', 'Joint 1 vel', 'Joint 2 vel', 'Joint 3 vel', 'Joint 4 vel', 'Joint 5 vel', 'Joint 6 vel'])
plt.title('Test 2: 0.3rad/sec2, 0.3rad/s, 2x overshoot')
plt.show()







