# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 13:20:00 2023

@author: nicho
"""

import numpy as np
import matplotlib.pyplot as plt

def newtons_method_visuals(f,tol,num_of_iterations,real_range,imag_range,num_of_points_each_direction,roots_graph=0,fractal=0,real_graph=0):
    """
    Parameters
    ----------
    f : Function of z
    
    tol : Tolerance of Newton's method formula
    
    num_of_iterations : Number of iterations of Newton's method formula
    
    real_range : Range on the real axis
    
    imag_range : Range on the imaginary axis
    
    num_of_points_each_direction : Number of points in each direction. The total number of points is this squared
    
    roots_graph : Binary, optional
        The display of the roots on the complex plane. The default is 0.
        
    fractal : Binary, optional
        The display of the fractal on the complex plane. The default is 0.
        
    real_graph : Binary, optional
        The display of the graph of the function on the real plane. The default is 0.

    Returns
    -------
    The complex roots of the function in a list, and the graphs if specified.

    """
    def newton_method(f,x0,tol,num_of_iterations):
        """
        Parameters
        ----------
        f : Function of x.
        
        x0 : Initial value of x.
        
        tol : Tolerance of Newton's method formula.
        
        num_of_iterations : Number of iterations of Newton's method formula

        Returns
        -------
        The root of the function at x0 according to Newton's method.

        """
        h = 10**(-8)
        df = lambda x: (f(x+h)-f(x))/h # calculate derivative
        l = []
        for n in range(num_of_iterations):
            l.append(x0) 
            if len(l) != len(set(l)):
                return 'Error' # if list of all values has duplicates, it is in a periodic loop and no solution will be found
            if df(x0) == 0:
                return 'Error' # if derivative at initial point equals 0, newton's method has no solution
            xn = x0 - f(x0)/df(x0) # newton's method formula
            finish = abs(xn-x0)
            if finish < tol:
                return xn # if the difference between two subsequent values is less than the tolerance, a solution has been found    
            x0 = xn
        return 'Error' # if the iteration finds no solution, then no solution has been found
    
    ans = lambda z0: newton_method(f,z0,tol,num_of_iterations) # a function where only the initial value changes
    
    n = num_of_points_each_direction
    x = np.linspace(real_range[0],real_range[1],n) # generate n values in the real range
    y = np.linspace(imag_range[0],imag_range[1],n) # generate n values in the imaginary range
    
    l = [] # combine these ranges to generate n^2 points on the complex plane in the ranges specified
    for i in range(len(x)):
        for j in range(len(y)):
            z = complex(x[i],y[j])
            l.append(z)
    
    roots1 = [] # calculate the root of every point in the list above
    for i in range(len(l)):
        roots1.append(ans(l[i]))
 
    error_indexes = [index for index, item in enumerate(roots1) if item == 'Error'] # get the index for every 'Error' in the roots 
    
    roots = [item for index, item in enumerate(roots1) if index not in error_indexes] # remove 'Error's from the roots
    
    error_indexes.sort(reverse=True) # Put error indexes in reverse order so that when removing these values later, it does not change the index values and remove the wrong values

    seperate_roots = [] # List for every unique root
    
    roots_index = [[root, 0] for root in roots] # Generate a vector of 0s next to each root. This will be changed later in order to colour code
  
    for j in range(len(roots)): # Test for unique roots and group all similar roots with the same 2nd column value
        num = 0
        for i in range(len(seperate_roots)):
            test = np.isclose(seperate_roots[i],roots[j]) # Test if a root in roots is close to any already known unique roots
            if test == 1: # If the root is close to a known unique root, set the associated vector to the same as the index value of the unique root it was close to.
                roots_index[j][1] = i
                num = num + 1
        if num == 0: # If the root is not close to any known unique root, put the root in the unique roots and set the vector to the associated index value
            roots_index[j][1] = len(seperate_roots)
            seperate_roots.append(roots[j])
            
    c = [item[1] for item in roots_index] # Take the vector values which associate close roots together
    cmap = plt.get_cmap('jet', np.max(c)+1) # Generate a colour map to differentiate the seperate roots
    s = 1/num_of_points_each_direction * 2000 # Set the dot size based upon the number of dots in the space
    
    if roots_graph == 1:
        
        x = [ele.real for ele in roots] # Take the real part of every root and plot it as x
        y = [ele.imag for ele in roots] # Take the imaginary part of every root and plot it as y
        
        plt.scatter(x,y,c=c,cmap=cmap) # Plot all roots with the colourmap based on the associative vector
        plt.title("Roots")
        plt.ylabel('Imaginary') 
        plt.xlabel('Real') 
        plt.xlim(min(x)-1,max(x)+1) # Set the real bounds to fit all roots on the plot
        plt.ylim(min(y)-1,max(y)+1) # Set the imaginary bounds to fit all roots on the plot
        plt.grid()
        plt.show()
    
    if fractal == 1:
        
        for index in error_indexes: # Remove all points from the initial points which have no solution
            if 0 <= index < len(l):
                l.pop(index)
        
        x = [ele.real for ele in l] # Take the real part of every initial value and plot it as x
        y = [ele.imag for ele in l] # Take the imaginary part of every initial value and plot it as x
        
        rootx = [ele.real for ele in seperate_roots] # Take the real parts of the seperate roots
        rooty = [ele.imag for ele in seperate_roots] # Take the imaginary parts of the seperate roots
        
        plt.scatter(x,y,c=c,cmap=cmap,s=s, marker='s') # Plot all initial values with the colourmap based on the associative vector, and plot the points as squares to reduce overlapping
        plt.scatter(rootx,rooty,color='black',s=100) # Plot the seperate roots in black
        plt.title("Fractal")
        plt.ylabel('Imaginary') 
        plt.xlabel('Real') 
        plt.xlim(real_range[0],real_range[1])
        plt.ylim(imag_range[0],imag_range[1])
        plt.show()
    
    if real_graph == 1:
        
        zero = lambda x: x-x # Function which returns 0
        x = np.linspace(real_range[0],real_range[1],num_of_points_each_direction)
        
        plt.plot(x,f(x)) # Plot the function used in the algorithm on the real plane
        plt.plot(x,zero(x),color='black',linewidth = 3,linestyle='dashed') # Plot a line at x=0
        plt.ylim(-5,5)
        plt.ylabel('x') 
        plt.xlabel('y') 
        plt.grid()
        plt.title('Real Plot of the Function')
        plt.show()
    
    return seperate_roots # Returns all unique roots

 
