import matplotlib.pyplot as plt
from settings import Settings
from tools import table

PLOT_ROW = 1
PLOT_COL = 2

def graphics_init():
    plt.ion()   # Necessary to get animation effect 
    plt.figure(figsize=[15,10])

def plot1(x):  
    plt.subplot(PLOT_ROW,PLOT_COL, 1)
    plt.title("This is plot 1")
    plt.plot(x)
    plt.xlabel("Periods")
    plt.ylabel("Number of persons")
    plt.xlim(0, Settings.number_of_periods) 

def plot2(x):  
    plt.subplot(PLOT_ROW,PLOT_COL, 2)
    plt.title("This id plot 2")
    a,n = table(x)
    plt.bar(a, n)
    plt.xlabel("Age")
    


