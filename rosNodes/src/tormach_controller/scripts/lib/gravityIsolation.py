import numpy as np
from math import sin, cos, pi
import csv
from scipy.optimize import least_squares
import math




def gravModle(x, q, tautrue):
    """ from Dr wen's matlab code:




0
-(g*(2*L5*m5*cos(q2 + q3) + 2*L5*m6*cos(q2 + q3) + 2*L4x*m4*cos(q2 + q3) + 2*L4x*m5*cos(q2 + q3) + 2*L4x*m6*cos(q2 + q3) + 2*Lc4*m4*cos(q2 + q3) + 2*Lc3a*m3*cos(q2 + q3) + 2*L4z*m4*sin(q2 + q3) + 2*L4z*m5*sin(q2 + q3) + 2*L4z*m6*sin(q2 + q3) + 2*Lc3c*m3*sin(q2 + q3) + 2*Lc2a*m2*cos(q2) + 2*L3*m3*sin(q2) + 2*L3*m4*sin(q2) + 2*L3*m5*sin(q2) + 2*L3*m6*sin(q2) + 2*Lc2c*m2*sin(q2) - L6*m6*sin(q2 + q3)*sin(q4 + q5) - Lc5*m5*sin(q2 + q3)*sin(q4 + q5) - Lc6*m6*sin(q2 + q3)*sin(q4 + q5) + 2*L6*m6*cos(q2 + q3)*cos(q5) + 2*Lc5*m5*cos(q2 + q3)*cos(q5) + 2*Lc6*m6*cos(q2 + q3)*cos(q5) + L6*m6*sin(q4 - q5)*sin(q2 + q3) + Lc5*m5*sin(q4 - q5)*sin(q2 + q3) + Lc6*m6*sin(q4 - q5)*sin(q2 + q3)))/2
-g*(L5*m5*cos(q2 + q3) + L5*m6*cos(q2 + q3) + L4x*m4*cos(q2 + q3) + L4x*m5*cos(q2 + q3) + L4x*m6*cos(q2 + q3) + Lc4*m4*cos(q2 + q3) + Lc3a*m3*cos(q2 + q3) + L4z*m4*sin(q2 + q3) + L4z*m5*sin(q2 + q3) + L4z*m6*sin(q2 + q3) + Lc3c*m3*sin(q2 + q3) + L6*m6*cos(q2 + q3)*cos(q5) + Lc5*m5*cos(q2 + q3)*cos(q5) + Lc6*m6*cos(q2 + q3)*cos(q5) - L6*m6*sin(q2 + q3)*cos(q4)*sin(q5) - Lc5*m5*sin(q2 + q3)*cos(q4)*sin(q5) - Lc6*m6*sin(q2 + q3)*cos(q4)*sin(q5))
g*cos(q2 + q3)*sin(q4)*sin(q5)*(L6*m6 + Lc5*m5 + Lc6*m6)
g*(L6*m6 + Lc5*m5 + Lc6*m6)*(cos(q2)*sin(q3)*sin(q5) + cos(q3)*sin(q2)*sin(q5) - cos(q2)*cos(q3)*cos(q4)*cos(q5) + cos(q4)*cos(q5)*sin(q2)*sin(q3))
0



    given L1,2...6,T from geometry
    data is taus and qs 
    loking for Lc's and m's

    input: x - a np array (length 12) in the order m1, m2, ... ,m6, Lc1, Lc2,...,Lc6
    output: tau - a np array (length 6) of the calculated joint torques
    """
    # define constants
    # gravity (m/s)
    g=9.81;
    L1=279
    L2x=25
    L2z=171
    L3=454
    L4z=35
    L4x=123
    L5=296.5
    L6=00
    LT=117.5

    #interperate inputs
    m1=x[0]
    m2=x[1]
    m3=x[2]
    m4=x[3]
    m5=x[4]
    m6=x[5]
    Lc1=x[6]
    Lc2a=x[7]
    Lc2b=x[8]
    Lc2c=x[9]
    Lc3a=x[10]
    Lc3b=x[11]
    Lc3c=x[12]
    Lc4=x[13]
    Lc5=x[14]
    Lc6=x[15]


    tau=np.zeros(1);
    # print(np.shape(q))
    for i in range(np.shape(q)[0]):

        q1=q[i,0]*pi/180
        q2=q[i,1]*pi/180
        q3=q[i,2]*pi/180
        q4=q[i,3]*pi/180
        q5=q[i,4]*pi/180
        q6=q[i,5]*pi/180
        temp=np.zeros(6)
        temp[0]=abs(-tautrue[i,0])
        temp[1]=abs(-tautrue[i,1] -(g*(2*L5*m5*cos(q2 + q3) + 2*L5*m6*cos(q2 + q3) + 2*L4x*m4*cos(q2 + q3) + 2*L4x*m5*cos(q2 + q3) + 2*L4x*m6*cos(q2 + q3) + 2*Lc4*m4*cos(q2 + q3) + 2*Lc3a*m3*cos(q2 + q3) + 2*L4z*m4*sin(q2 + q3) + 2*L4z*m5*sin(q2 + q3) + 2*L4z*m6*sin(q2 + q3) + 2*Lc3c*m3*sin(q2 + q3) + 2*Lc2a*m2*cos(q2) + 2*L3*m3*sin(q2) + 2*L3*m4*sin(q2) + 2*L3*m5*sin(q2) + 2*L3*m6*sin(q2) + 2*Lc2c*m2*sin(q2) - L6*m6*sin(q2 + q3)*sin(q4 + q5) - Lc5*m5*sin(q2 + q3)*sin(q4 + q5) - Lc6*m6*sin(q2 + q3)*sin(q4 + q5) + 2*L6*m6*cos(q2 + q3)*cos(q5) + 2*Lc5*m5*cos(q2 + q3)*cos(q5) + 2*Lc6*m6*cos(q2 + q3)*cos(q5) + L6*m6*sin(q4 - q5)*sin(q2 + q3) + Lc5*m5*sin(q4 - q5)*sin(q2 + q3) + Lc6*m6*sin(q4 - q5)*sin(q2 + q3)))/2)
        temp[2]=abs(-tautrue[i,2]-g*(L5*m5*cos(q2 + q3) + L5*m6*cos(q2 + q3) + L4x*m4*cos(q2 + q3) + L4x*m5*cos(q2 + q3) + L4x*m6*cos(q2 + q3) + Lc4*m4*cos(q2 + q3) + Lc3a*m3*cos(q2 + q3) + L4z*m4*sin(q2 + q3) + L4z*m5*sin(q2 + q3) + L4z*m6*sin(q2 + q3) + Lc3c*m3*sin(q2 + q3) + L6*m6*cos(q2 + q3)*cos(q5) + Lc5*m5*cos(q2 + q3)*cos(q5) + Lc6*m6*cos(q2 + q3)*cos(q5) - L6*m6*sin(q2 + q3)*cos(q4)*sin(q5) - Lc5*m5*sin(q2 + q3)*cos(q4)*sin(q5) - Lc6*m6*sin(q2 + q3)*cos(q4)*sin(q5)))
        temp[3]=abs(-tautrue[i,3]+g*cos(q2 + q3)*sin(q4)*sin(q5)*(L6*m6 + Lc5*m5 + Lc6*m6))
        temp[4]= abs(-tautrue[i,4]+g*(L6*m6 + Lc5*m5 + Lc6*m6)*(cos(q2)*sin(q3)*sin(q5) + cos(q3)*sin(q2)*sin(q5) - cos(q2)*cos(q3)*cos(q4)*cos(q5) + cos(q4)*cos(q5)*sin(q2)*sin(q3)))
        temp[5]=abs(-tautrue[i,5])
        tau=np.append(tau,temp,axis=0)

    return tau


def adjustTau(x, q, tautrue):
    """ from Dr wen's matlab code:




0
-(g*(2*L5*m5*cos(q2 + q3) + 2*L5*m6*cos(q2 + q3) + 2*L4x*m4*cos(q2 + q3) + 2*L4x*m5*cos(q2 + q3) + 2*L4x*m6*cos(q2 + q3) + 2*Lc4*m4*cos(q2 + q3) + 2*Lc3a*m3*cos(q2 + q3) + 2*L4z*m4*sin(q2 + q3) + 2*L4z*m5*sin(q2 + q3) + 2*L4z*m6*sin(q2 + q3) + 2*Lc3c*m3*sin(q2 + q3) + 2*Lc2a*m2*cos(q2) + 2*L3*m3*sin(q2) + 2*L3*m4*sin(q2) + 2*L3*m5*sin(q2) + 2*L3*m6*sin(q2) + 2*Lc2c*m2*sin(q2) - L6*m6*sin(q2 + q3)*sin(q4 + q5) - Lc5*m5*sin(q2 + q3)*sin(q4 + q5) - Lc6*m6*sin(q2 + q3)*sin(q4 + q5) + 2*L6*m6*cos(q2 + q3)*cos(q5) + 2*Lc5*m5*cos(q2 + q3)*cos(q5) + 2*Lc6*m6*cos(q2 + q3)*cos(q5) + L6*m6*sin(q4 - q5)*sin(q2 + q3) + Lc5*m5*sin(q4 - q5)*sin(q2 + q3) + Lc6*m6*sin(q4 - q5)*sin(q2 + q3)))/2
-g*(L5*m5*cos(q2 + q3) + L5*m6*cos(q2 + q3) + L4x*m4*cos(q2 + q3) + L4x*m5*cos(q2 + q3) + L4x*m6*cos(q2 + q3) + Lc4*m4*cos(q2 + q3) + Lc3a*m3*cos(q2 + q3) + L4z*m4*sin(q2 + q3) + L4z*m5*sin(q2 + q3) + L4z*m6*sin(q2 + q3) + Lc3c*m3*sin(q2 + q3) + L6*m6*cos(q2 + q3)*cos(q5) + Lc5*m5*cos(q2 + q3)*cos(q5) + Lc6*m6*cos(q2 + q3)*cos(q5) - L6*m6*sin(q2 + q3)*cos(q4)*sin(q5) - Lc5*m5*sin(q2 + q3)*cos(q4)*sin(q5) - Lc6*m6*sin(q2 + q3)*cos(q4)*sin(q5))
g*cos(q2 + q3)*sin(q4)*sin(q5)*(L6*m6 + Lc5*m5 + Lc6*m6)
g*(L6*m6 + Lc5*m5 + Lc6*m6)*(cos(q2)*sin(q3)*sin(q5) + cos(q3)*sin(q2)*sin(q5) - cos(q2)*cos(q3)*cos(q4)*cos(q5) + cos(q4)*cos(q5)*sin(q2)*sin(q3))
0



    given L1,2...6,T from geometry
    data is taus and qs 
    loking for Lc's and m's

    input: x - a np array (length 12) in the order m1, m2, ... ,m6, Lc1, Lc2,...,Lc6
    output: tau - a np array (length 6) of the calculated joint torques
    """
    # define constants
    # gravity (m/s)
    g=9.81;
    L1=279
    L2x=25
    L2z=171
    L3=454
    L4z=35
    L4x=123
    L5=296.5
    L6=000
    LT=117.5

    #interperate inputs
    m1=x[0]
    m2=x[1]
    m3=x[2]
    m4=x[3]
    m5=x[4]
    m6=x[5]
    Lc1=x[6]
    Lc2a=x[7]
    Lc2b=x[8]
    Lc2c=x[9]
    Lc3a=x[10]
    Lc3b=x[11]
    Lc3c=x[12]
    Lc4=x[13]
    Lc5=x[14]
    Lc6=x[15]


    tau=np.zeros(6);
    # print(np.shape(q))


    q1=q[0]*pi/180
    q2=q[1]*pi/180
    q3=q[2]*pi/180
    q4=q[3]*pi/180
    q5=q[4]*pi/180
    q6=q[5]*pi/180
    # temp=np.zeros(6)
    tau[0]=-tautrue[0]
    tau[1]=-tautrue[1] -(g*(2*L5*m5*cos(q2 + q3) + 2*L5*m6*cos(q2 + q3) + 2*L4x*m4*cos(q2 + q3) + 2*L4x*m5*cos(q2 + q3) + 2*L4x*m6*cos(q2 + q3) + 2*Lc4*m4*cos(q2 + q3) + 2*Lc3a*m3*cos(q2 + q3) + 2*L4z*m4*sin(q2 + q3) + 2*L4z*m5*sin(q2 + q3) + 2*L4z*m6*sin(q2 + q3) + 2*Lc3c*m3*sin(q2 + q3) + 2*Lc2a*m2*cos(q2) + 2*L3*m3*sin(q2) + 2*L3*m4*sin(q2) + 2*L3*m5*sin(q2) + 2*L3*m6*sin(q2) + 2*Lc2c*m2*sin(q2) - L6*m6*sin(q2 + q3)*sin(q4 + q5) - Lc5*m5*sin(q2 + q3)*sin(q4 + q5) - Lc6*m6*sin(q2 + q3)*sin(q4 + q5) + 2*L6*m6*cos(q2 + q3)*cos(q5) + 2*Lc5*m5*cos(q2 + q3)*cos(q5) + 2*Lc6*m6*cos(q2 + q3)*cos(q5) + L6*m6*sin(q4 - q5)*sin(q2 + q3) + Lc5*m5*sin(q4 - q5)*sin(q2 + q3) + Lc6*m6*sin(q4 - q5)*sin(q2 + q3)))/2
    tau[2]=-tautrue[2]-g*(L5*m5*cos(q2 + q3) + L5*m6*cos(q2 + q3) + L4x*m4*cos(q2 + q3) + L4x*m5*cos(q2 + q3) + L4x*m6*cos(q2 + q3) + Lc4*m4*cos(q2 + q3) + Lc3a*m3*cos(q2 + q3) + L4z*m4*sin(q2 + q3) + L4z*m5*sin(q2 + q3) + L4z*m6*sin(q2 + q3) + Lc3c*m3*sin(q2 + q3) + L6*m6*cos(q2 + q3)*cos(q5) + Lc5*m5*cos(q2 + q3)*cos(q5) + Lc6*m6*cos(q2 + q3)*cos(q5) - L6*m6*sin(q2 + q3)*cos(q4)*sin(q5) - Lc5*m5*sin(q2 + q3)*cos(q4)*sin(q5) - Lc6*m6*sin(q2 + q3)*cos(q4)*sin(q5))
    tau[3]=-tautrue[3]+g*cos(q2 + q3)*sin(q4)*sin(q5)*(L6*m6 + Lc5*m5 + Lc6*m6)
    tau[4]= -tautrue[4]+g*(L6*m6 + Lc5*m5 + Lc6*m6)*(cos(q2)*sin(q3)*sin(q5) + cos(q3)*sin(q2)*sin(q5) - cos(q2)*cos(q3)*cos(q4)*cos(q5) + cos(q4)*cos(q5)*sin(q2)*sin(q3))
    tau[5]=-tautrue[5]
    

    return -1*tau


def calibrate(csvFile):
    # open file
    q=np.zeros((1,6))
    tau=np.zeros((1,6))

    with open(csvFile, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            temp=np.array([[float(row[0].split('(')[1]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5].split(')')[0])]])
            # print(temp)
            q=np.append(q,temp, axis=0)
            temp=[[float(row[6].split('(')[1]),float(row[7]),float(row[8]),float(row[9]),float(row[10]),float(row[11].split(')')[0])]]
            tau=np.append(tau,temp, axis=0)

        # print(q[1:])
        # reader.close()
        obj=lambda x: gravModle(x,q[1:],tau[1:]);
        x0=np.ones(16)
        res = least_squares(obj, x0, args=())
        # print(res.x)
        adjustedTau= lambda q, tau: adjustTau(res.x,q,tau);
        # print(adjustedTau(q[1],tau[1]))
        # print(tau[1])
        # print(adjustedTau(q[2],tau[2]))
        # print(tau[2])
        # print(adjustedTau(q[3],tau[3]))
        # print(tau[3])

        return adjustedTau


# calibrate("gravityIsolationData.csv")