import matplotlib.pyplot as plt
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
    plt.xlabel("gamma")
    plt.ylabel("Discounted profits")
    # plt.xlim(0, Settings.number_of_periods) 
    # 
    plt.ylim(-200, 300) 


def plot3(x,y):
    plt.subplot(2,3,3)
    #plt.title(title)
    plt.plot(x,y, 'o', ms=0.5)
    plt.xlabel("S")
    plt.ylabel("Discounted utility")
    # plt.xlim(0, Settings.number_of_periods) 
    #plt.ylim(250000, 1000) 

def plot4(x):
    plt.subplot(2,3,4)
    #plt.title(title)
    plt.hist(x)
    plt.xlabel("L")
    #plt.ylabel("Discounted utility")
    # plt.xlim(0, Settings.number_of_periods) 
    #plt.ylim(-250000,1000) 

def plot5(x):
    xx = []
    for s in x:
        if s < 10:
            xx.append(s)
    plt.subplot(2,3,5)
    #plt.title(title)
    plt.hist(xx)
    plt.xlabel("Unempl_duration")
    #plt.ylabel("Discounted utility")
    # plt.xlim(0, Settings.number_of_periods) 
    #plt.ylim(-250000,1000) 

