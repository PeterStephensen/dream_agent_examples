import matplotlib.pyplot as plt
import numpy as np

from collections import Counter
from settings import Settings

from dream_agent import local_mean

def graphics_init():
    plt.ion()   # Necessary to get animation effect 
    plt.figure(figsize=[15,10])

PLOT_ROW = 2
PLOT_COL = 4

def plot1(x):
    plt.subplot(PLOT_ROW,PLOT_COL,1)
    #plt.title(title)
    plt.plot(x)
    plt.xlabel("Periods")
    plt.ylabel("Total employment")
    plt.xlim(0, Settings.number_of_periods) 
    
    n = Settings.number_of_workplaces*Settings.number_of_workers_per_workplace
    plt.ylim(0.5*n, 1.1*n) 

def plot2(x,y):
    plt.subplot(PLOT_ROW,PLOT_COL,2)
    #plt.title(title)
    plt.plot(x,y, 'o', ms=3)
    xx, yy = local_mean(x, y, n=15)
    plt.plot(xx,yy, color="red")
    plt.xlabel("gamma")
    plt.ylabel("Discounted profits")
    # plt.xlim(0, Settings.number_of_periods) 
    # 
    # plt.ylim(-200, 300) 


def plot3(x,y):
    plt.subplot(PLOT_ROW,PLOT_COL,3)
    #plt.title(title)
    plt.plot(x,y, 'o', ms=0.5)
    xx,yy = local_mean(x, y, n=30)
    plt.plot(xx,yy, color="red")
    plt.xlabel("S")
    plt.ylabel("Discounted utility")
    # plt.xlim(0, Settings.number_of_periods) 
    # plt.ylim(250000, 1000) 

def plot4(x):
    plt.subplot(PLOT_ROW,PLOT_COL,4)
    #plt.title(title)
    plt.hist(x)
    plt.xlabel("L")
    #plt.ylabel("Discounted utility")
    # plt.xlim(0, Settings.number_of_periods) 
    #plt.ylim(-250000,1000) 


def plot5(x):
    c = Counter(x)
    x, n = list(c), list(c.values())

    plt.subplot(PLOT_ROW,PLOT_COL,5)
    #plt.title(title)
    plt.bar(x, n, width=0.5) 
    plt.xlabel("Unemployment duration")
    #plt.ylabel("Discounted utility")
    plt.xlim(0, 50) 
    #plt.ylim(-250000,1000) 

def plot6(x):
    plt.subplot(PLOT_ROW,PLOT_COL,6)
    #plt.title(title)
    plt.plot(x)
    plt.xlabel("Periods")
    plt.ylabel("Best S")
    plt.xlim(0, Settings.number_of_periods)     
    plt.ylim(0, 4) 

def plot7(x):
    plt.subplot(PLOT_ROW,PLOT_COL,7)
    #plt.title(title)
    plt.plot(x)
    plt.xlabel("Periods")
    plt.ylabel("Best gamma")
    plt.xlim(0, Settings.number_of_periods)     
    plt.ylim(0, 1) 

def plot8(x):
    plt.subplot(PLOT_ROW,PLOT_COL,8)
    #plt.title(title)
    plt.plot(x)
    plt.xlabel("Periods")
    plt.ylabel("Unemployed")
    plt.xlim(0, Settings.number_of_periods)     
    plt.ylim(0, 10000) 
