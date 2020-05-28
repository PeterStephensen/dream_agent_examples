import matplotlib.pyplot as plt
import numpy as np

from collections import Counter
from settings import Settings

def graphics_init():
    plt.ion()   # Necessary to get animation effect 
    plt.figure(figsize=[15,10])

def plot1(x):
    plt.subplot(2,3,1)
    #plt.title(title)
    plt.plot(x)
    plt.xlabel("Periods")
    plt.ylabel("Total employment")
    plt.xlim(0, Settings.number_of_periods) 
    
    n = Settings.number_of_workplaces*Settings.number_of_workers_per_workplace
    plt.ylim(0.5*n, 1.1*n) 

def plot2(x,y):
    plt.subplot(2,3,2)
    #plt.title(title)
    plt.plot(x,y, 'o', ms=3)
    xx, yy = local_avr(x, y, n=15)
    plt.plot(xx,yy, color="red")
    plt.xlabel("gamma")
    plt.ylabel("Discounted profits")
    # plt.xlim(0, Settings.number_of_periods) 
    # 
    #plt.ylim(-200, 300) 


def plot3(x,y):
    plt.subplot(2,3,3)
    #plt.title(title)
    plt.plot(x,y, 'o', ms=0.5)
    xx,yy = local_avr(x, y, n=30)
    plt.plot(xx,yy, color="red")
    plt.xlabel("S")
    plt.ylabel("Discounted utility")
    # plt.xlim(0, Settings.number_of_periods) 
    # plt.ylim(250000, 1000) 

def plot4(x):
    plt.subplot(2,3,4)
    #plt.title(title)
    plt.hist(x)
    plt.xlabel("L")
    #plt.ylabel("Discounted utility")
    # plt.xlim(0, Settings.number_of_periods) 
    #plt.ylim(-250000,1000) 


def plot5(x):
    c = Counter(x)
    x, n = list(c), list(c.values())

    plt.subplot(2,3,5)
    #plt.title(title)
    plt.bar(x, n, width=0.5) 
    plt.xlabel("Unemployment duration")
    #plt.ylabel("Discounted utility")
    plt.xlim(0, 50) 
    #plt.ylim(-250000,1000) 


# Poor man's loess 
def local_avr(x,y, n=10):
    x, y = (list(t) for t in zip(*sorted(zip(x, y))))
    mn, mx  = min(x), max(x) 
    seq = np.linspace(mn,mx,n+1)

    x_o, y_o = [], []
    x_avr, y_avr = [], []
    j=1
    for i in range(len(x)):
        if x[i] < seq[j]:
            x_avr.append(x[i])
            y_avr.append(y[i])
        else:
            x_o.append(sum(x_avr)/len(x_avr))
            y_o.append(sum(y_avr)/len(y_avr))
            x_avr, y_avr = [], []
            j += 1

    return x_o, y_o 

