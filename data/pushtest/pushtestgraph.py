import numpy as np
import matplotlib.pyplot as plt

def getMeasures(filename):
	c=0
	data=[[],[],[],[],[],[]]
	with open(filename, 'r') as file:
		for line in file:
		# print(line.strip())
			temp=line.strip()
			if not (c%7)==6: #velocity
				temp=temp.split(':')[1]
				temp=np.array(temp, dtype=float)
				data[c%7].append(temp)

			c+=1
	return np.array(data)


filename='filename.txt'

y=getMeasures(filename)

t=np.linspace(0,y.shape[1],y.shape[1])/25


fig, ax = plt.subplots(2)
for i in range(3):
	ax[0].plot(t,y[i,:])
	ax[1].plot(t,y[3+i,:])

# ax[0].plot(shit1)
# ax[1].plot(shit2)
plt.legend(['Force x', 'Force y', 'Force z', 'Moment x', 'Moment y','Moment z'])
plt.show()