import matplotlib.pyplot as plt
from settings import Settings
from tools import table

PLOT_ROW = 2
PLOT_COL = 4

def graphics_init():
    plt.ion()   # Necessary to get animation effect 
    plt.figure(figsize=[17,10])

def plot1(x):  
    """Plotting time series of number of firms"""
    plt.subplot(PLOT_ROW,PLOT_COL, 1)
    #plt.title("This is plot 1")
    plt.plot(x)
    plt.xlabel("Periods")
    plt.ylabel("Number of firms")
    plt.xlim(0, Settings.number_of_periods) 
    # plt.ylim(0, 2*Settings.number_of_firms) 

def plot2(x):  
    """Histogram of productivity"""
    plt.subplot(PLOT_ROW,PLOT_COL, 2)
    #plt.title("distribution")
    plt.hist(x, bins=15)
    plt.xlabel("Productivity")
    plt.xlim(0, 2) 
    
def plot3(x):  
    """Plotting times series of mean_wage"""
    plt.subplot(PLOT_ROW,PLOT_COL, 3)
    #plt.title("This is plot 1")
    plt.plot(x)
    plt.xlabel("Periods")
    plt.ylabel("Mean wage")
    plt.xlim(0, Settings.number_of_periods) 
    # plt.ylim(0, 2) 

def plot4(x):  
    """Plotting time series of number of employed in the economy"""
    plt.subplot(PLOT_ROW,PLOT_COL, 4)
    #plt.title("This is plot 1")
    plt.plot(x)
    plt.xlabel("Periods")
    plt.ylabel("Number of employed")
    plt.xlim(0, Settings.number_of_periods) 
    # plt.ylim(0, 2*Settings.number_of_firms) 

def plot5(x):  
    """Histogram of profit"""
    plt.subplot(PLOT_ROW,PLOT_COL, 5)
    #plt.title("distribution")
    plt.hist(x, bins=15)
    plt.xlabel("Profit")
    # plt.xlim(0, 2) 

def plot6(x):  
    """Histogram of reserve"""
    plt.subplot(PLOT_ROW,PLOT_COL, 6)
    #plt.title("distribution")
    plt.hist(x, bins=15)
    plt.xlabel("Reserve")
    # plt.xlim(0, 2) 

def plot7(x):  
    """Histogram of wage"""
    plt.subplot(PLOT_ROW,PLOT_COL, 7)
    #plt.title("distribution")
    plt.hist(x, bins=15)
    plt.xlabel("Wage")
    # plt.xlim(0, 2) 

# def plot3(x):  
#     plt.subplot(PLOT_ROW,PLOT_COL, 2)
#     plt.title("This id plot 2")
#     a,n = table(x)
#     plt.bar(a, n)
#     plt.xlabel("Age")


