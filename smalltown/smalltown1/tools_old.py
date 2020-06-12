# usefull python functions and classes

from collections import Counter

# Table function
def table(x):
    """Table function a la R for integer values

    Arguments:
        x {list} -- List of integers

    Returns:
        {list, list} -- Two lists. First list is integer values. 
                      Second list i number of occurrences of each value
    """
    c = Counter(x)
    return list(c), list(c.values())

# Usefull function
def exist(x):
    """Tests whether an object is allocated

    Args:
        x (object): Any object

    Returns:
        bool: True if 'not None'
    """
    return x is not None


# Poor man's loess. Fine and quick if many data points 
def local_mean(x,y, n=10):
    """Calculating local means. Poor man's loess. Fine and quick if many data points. 
    The algorithm works like this:
          1) x and y are sorted according to x, 
          2) the data is split in n equally sized parts, and
          3) means are calculated for both x and y in each part.     

    Arguments:
        x {list} -- The x data
        y {list} -- The y data

    Keyword Arguments:
        n {int} -- The number of parts (default: {10})

    Returns:
        {list, list} -- n mean values of x and y
    """

    xx, yy = (list(t) for t in zip(*sorted(zip(x, y)))) # sort x and y after x

    m = int(len(x)/n) # Number of data points in each group

    x_o, y_o = [], []
    x_sum, y_sum, v = 0, 0, 0
    j=1
    for i in range(len(x)):
        if v < m:
            x_sum += xx[i]
            y_sum += yy[i]
            v += 1
        else:
            x_o.append(x_sum/m)
            y_o.append(y_sum/m)
            x_sum, y_sum, v = 0, 0, 0
            j += 1

    return x_o, y_o 

