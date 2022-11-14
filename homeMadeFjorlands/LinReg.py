import pandas as pd
import numpy as np

matrix = np.array(A.values,'float')
matrix[0:5,:]    #first 5 rows of data
data = np.array([[194.33333333,   7.526     ],
       [188.33333333,   7.509     ],
       [124.        ,   7.501     ],
       [123.        ,   7.498     ],
       [164.33333333,   7.413     ]])

X = matrix[:,0]
y = matrix[:,1]

X = X/(np.max(X)) 

import matplotlib.pyplot as plt
plt.plot(X,y,'bo')
plt.ylabel('Happiness Score')
plt.xlabel('Alcohol consumption')
plt.legend(['Happiness Score'])
plt.title('Alcohol_Vs_Happiness')
plt.grid()
plt.show()

def computecost(x,y,theta):
    
    a = 1/(2*m)
    b = np.sum(((x@theta)-y)**2)
    j = (a)*(b)
    return j

print(computecost(x,y,theta))

#initialising parameter
m = np.size(y)
X = X.reshape([122,1])
x = np.hstack([np.ones_like(X),X])
theta = np.zeros([2,1])
print(theta,'\n',m)

def gradient(x,y,theta):
    
    alpha = 0.00001
    iteration = 2000
#gradient descend algorithm
    J_history = np.zeros([iteration, 1]);
    for iter in range(0,2000):
        
        error = (x @ theta) -y
        temp0 = theta[0] - ((alpha/m) * np.sum(error*x[:,0]))
        temp1 = theta[1] - ((alpha/m) * np.sum(error*x[:,1]))
        theta = np.array([temp0,temp1]).reshape(2,1)
        J_history[iter] = (1 / (2*m) ) * (np.sum(((x @ theta)-y)**2))   #compute J value for each iteration 
    return theta, J_history

theta , J = gradient(x,y,theta)
print(theta)

theta , J = gradient(x,y,theta)
print(J)

#plot linear fit for our theta
plt.plot(X,y,'bo')
plt.plot(X,x@theta,'-')
plt.axis([0,1,3,7])
plt.ylabel('Happiness Score')
plt.xlabel('Alcohol consumption')
plt.legend(['HAPPY','LinearFit'])
plt.title('Alcohol_Vs_Happiness')
plt.grid()
plt.show()

predict1 = [1,(164/np.max(matrix[:,0]))] @ theta #normalising the input value, 1 is for intercept term so not need to normalise
print(predict1)