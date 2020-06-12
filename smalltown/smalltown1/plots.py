import matplotlib.pyplot as plt

from tools import table

from .settings import Settings

PLOT_ROW = 2
PLOT_COL = 6

def graphics_init():
    plt.ion()   # Necessary to get animation effect 
    plt.figure(figsize=[18,8])

def plot1(x):  
    """Plotting time series of number of firms"""    
    plt.subplot(PLOT_ROW,PLOT_COL, 1)
    plt.title("Number of firms")
    plt.plot(x)
    plt.xlabel("Periods")
    # plt.ylabel("Number of firms")
    plt.xlim(0, Settings.number_of_periods) 
    plt.ylim(0, 1.1*max(x)) 

def plot2(x):  
    """Histogram of productivity"""
    plt.subplot(PLOT_ROW,PLOT_COL, 2)
    plt.title("Productivity")
    plt.hist(x, bins=15)
    # plt.xlabel("Productivity")
    plt.xlim(0, 4) 
    
def plot3(x):  
    """Plotting times series of mean_wage"""
    plt.subplot(PLOT_ROW,PLOT_COL, 3)
    plt.title("Mean wage")
    plt.plot(x)
    plt.xlabel("Periods")
    # plt.ylabel("Mean wage")
    plt.xlim(0, Settings.number_of_periods) 
    # plt.ylim(0, 2) 

def plot4(x):  
    """Plotting time series of number of employed in the economy"""
    plt.subplot(PLOT_ROW,PLOT_COL, 4)
    plt.title("Number of employed")
    plt.plot(x)
    plt.xlabel("Periods")
    # plt.ylabel("Number of employed")
    plt.xlim(0, Settings.number_of_periods) 
    # plt.ylim(0, 400) 

def plot5(x):  
    """Histogram of profit"""
    plt.subplot(PLOT_ROW,PLOT_COL, 5)
    #plt.title("distribution")
    plt.hist(x, bins=15)
    plt.xlabel("Firm: Profit")
    # plt.xlim(0, 2) 

def plot6(x):  
    """Histogram of reserve"""
    plt.subplot(PLOT_ROW,PLOT_COL, 6)
    #plt.title("distribution")
    plt.hist(x, bins=15)
    plt.xlabel("Firm: Reserve")
    # plt.xlim(0, 2) 

def plot7(x):  
    """Histogram of wage"""
    plt.subplot(PLOT_ROW,PLOT_COL, 7)
    #plt.title("distribution")
    plt.hist(x, bins=15)
    plt.xlabel("Firm: Wage")
    # plt.xlim(0, 2) 

def plot8(x):  
    """Table-plot of household search duration"""
    plt.subplot(PLOT_ROW,PLOT_COL, 8)
    # plt.title("This id plot 2")
    a,n = table(x)
    plt.bar(a, n)
    plt.xlabel("Household: Search duration")

def plot9(x):  
    """Table-plot of firm vacancies"""
    plt.subplot(PLOT_ROW,PLOT_COL, 9)
    # plt.title("This id plot 2")
    a,n = table(x)
    plt.bar(a, n)
    plt.xlabel("Firm: Vacancies")

def plot10(x):  
    """Table-plot of firm employment"""
    plt.subplot(PLOT_ROW,PLOT_COL, 10)
    # plt.title("This id plot 2")
    a,n = table(x)
    plt.bar(a, n)
    plt.xlabel("Firm: Employed")

def plot11(x):  
    """Plotting time series of total production"""
    plt.subplot(PLOT_ROW,PLOT_COL, 11)
    plt.title("Total production")
    plt.plot(x)
    plt.xlabel("Periods")
    # plt.ylabel("Number of firms")
    plt.xlim(0, Settings.number_of_periods) 
    # plt.ylim(0, 2*Settings.number_of_firms) 

def plot12(x):  
    """Plotting time series of defaults"""
    plt.subplot(PLOT_ROW,PLOT_COL, 12)
    plt.title("Number of defaults")
    plt.plot(x)
    plt.xlabel("Periods")
    # plt.ylabel("Number of firms")
    plt.xlim(0, Settings.number_of_periods) 
    # plt.ylim(0, 2*Settings.number_of_firms) 



