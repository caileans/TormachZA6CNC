import numpy as np
import matplotlib.pyplot as plt
time=np.array([])
pose=np.array([[0,0]])
vel=np.array([[0,0]])
eff=np.array([[0,0]])
initialTime=0;

c=1;
with open('file1.txt', 'r') as file:
	for line in file:
		# print(line.strip())
		temp=line.strip()
		if (c%19)==4:
			temp=float(temp.split(':')[1].split(' ')[-1]);
			if c==4:
				initialTime=temp;			
			time=np.append(time,temp)
		elif (c%19)==5:
			temp=float(temp.split(':')[1].split(' ')[-1]);
			if c==5:
				initialTime+=temp/10.0**9
			time[-1]+= temp/10.0**9 - initialTime
		elif (c%19)==16:
			temp=temp.split('[')[1].split(',')
			pose=np.append(pose,[[float(temp[0]),float(temp[1])]], axis=0)
		elif (c%19)==17:
			temp=temp.split('[')[1].split(',')
			vel=np.append(vel,[[float(temp[0]),float(temp[1])]], axis=0)
		elif(c%19)==18:
			temp=temp.split('[')[1].split(',')
			eff=np.append(eff,[[float(temp[0]),float(temp[1])]], axis=0)
		c+=1
print(initialTime)

# print(pose)

plt.plot(time, pose[1:,0], 'b')
plt.plot(time,pose[1:,1],'g')
plt.axis((11.5,16.5,-.2,.3))
plt.ylabel('Joint Postition (rad)')
plt.xlabel('Time (s)')
plt.legend(['Joint 1', 'Joint 2'])
plt.title('Position vs Time, Interupted Moves')
plt.show()


plt.plot(time, vel[1:,0], 'b')
plt.plot(time,vel[1:,1],'g')
plt.axis((11.5,16.5,-.35,.35))
plt.ylabel('Joint Velocity')
plt.xlabel('Time (s)')
plt.legend(['Joint 1', 'Joint 2'])
plt.title('Velocity vs Time, Interupted Moves')
plt.show()

plt.plot(time, vel[1:,0], 'b')
# plt.plot(time,vel[1:,1],'g')
plt.axis((12.23,12.36,-.05,.3))
plt.ylabel('Joint Velocity')
plt.xlabel('Time (s)')
plt.legend(['Joint 1', 'Joint 2'])
plt.title('Velocity vs Time, Interupted Moves Zoomed')
plt.show()

plt.plot(time, eff[1:,0], 'b')
plt.plot(time,eff[1:,1],'g')
plt.axis((11.5,16.5,-165,160))
plt.ylabel('Joint Effort')
plt.xlabel('Time (s)')
plt.legend(['Joint 1', 'Joint 2'])
plt.title('Effort vs Time, Interupted Moves')
plt.show()