import matplotlib.pyplot as plt

def graphics_init():
    plt.ion()   # Necessary to get animation effect 
    plt.figure(figsize=[8,8])

def plot1(x1,y1, x2, y2, t):
    plot_args = {'markersize': 6, 'alpha': 0.6}
    plt.title("Schelling - Network. Period {}".format(t))
    plt.plot(x1, y1, 'o', markerfacecolor='orange', **plot_args)
    plt.plot(x2, y2, 'o', markerfacecolor='green', **plot_args)    
