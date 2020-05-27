import matplotlib.pyplot as plt
from settings import Settings


def graphics_init():
    plt.ion()   # Necessary to get animation effect 
    plt.figure(figsize=[15,8])

def plot1(x):
    plt.subplot(2,2,1)
    #plt.title(title)
    plt.plot(x)
    plt.xlabel("Periods")
    plt.ylabel("Total employment")
    plt.xlim(0, Settings.number_of_periods) 
    
    n = Settings.number_of_workplaces*Settings.number_of_workers_per_workplace
    plt.ylim(0.5*n, 1.1*n) 

def plot2(x,y):
    plt.subplot(2,2,2)
    #plt.title(title)
    plt.plot(x,y, 'o', ms=3)
    plt.xlabel("gamma")
    plt.ylabel("Discounted profits")
    # plt.xlim(0, Settings.number_of_periods) 
    # plt.ylim(-200, 1000) 


def plot3(x,y):
    plt.subplot(2,2,3)
    #plt.title(title)
    plt.plot(x,y, 'o', ms=0.5)
    plt.xlabel("S")
    plt.ylabel("Discounted utility")
    # plt.xlim(0, Settings.number_of_periods) 
    #plt.ylim(ymin=-250000) 

def plot4(x):
    plt.subplot(2,2,4)
    #plt.title(title)
    plt.hist(x)
    plt.xlabel("L")
    #plt.ylabel("Discounted utility")
    # plt.xlim(0, Settings.number_of_periods) 
    #plt.ylim(ymin=-250000) 

    #    plt.subplot(1,2,2)
        # plt.title("Histogram of wealth")
        #plt.plot(x2, bins = range(10), align='left', rwidth=0.3)
        #plt.xlabel("Wealth")
        #plt.ylabel("Number")
        #plt.xlim(-0.2, 9) 
        #plt.ylim(0.0, 1.0) 

    # plt.subplot(2,2,3)
    # plt.title("Random persons wealth")
    # plt.plot(x3)
    # plt.xlabel("Periods")
    # plt.ylabel("Wealth")
    # plt.xlim(0, Settings.number_of_periods) 
    # #plt.ylim(0.0, 1.0) 

    # plt.subplot(2,2,4)
    # plt.title("Grid")
    # plt.imshow(x4, interpolation='nearest')
    # plt.colorbar()
