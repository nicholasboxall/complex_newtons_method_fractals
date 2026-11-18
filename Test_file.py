# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 00:11:34 2023

@author: nicho
"""

"""
Set Directory
"""

import os
os.chdir(os.path.dirname(__file__)) # Set the directory as the same as this files location 

"""
Imports
"""

import numpy as np
import newtons_method_imag_function as nmif
import matplotlib.pyplot as plt

plt.rcParams['figure.dpi'] = 800 # Set plotting quality higher than default

"""
Tests below. Unhash print to run code.
"""

"""
Test 1

Shows construction of graphs
"""

f = lambda z: z**2 + 1
tol = 10**(-4)
num_of_iterations = 100
real_range = [-2,2]
imag_range = [-2,2]
num_of_points_each_direction = 15

#print(nmif.newtons_method_visuals(f,tol,num_of_iterations,real_range,imag_range,num_of_points_each_direction,roots_graph=1,fractal=1,real_graph=1))

"""
Test 2

Function where 0 and 1 are in a periodic loop
"""

f = lambda z: z**3 - 2*z + 2
tol = 10**(-4)
num_of_iterations = 100
real_range = [-2,2]
imag_range = [-2,2]
num_of_points_each_direction = 175

#print(nmif.newtons_method_visuals(f,tol,num_of_iterations,real_range,imag_range,num_of_points_each_direction,roots_graph=1,fractal=1,real_graph=1))

"""
Test 3

High power polynomial with low iterations for newton's method
"""

f = lambda z: -16 + 15*z**4 + z**8
tol = 10**(-4)
num_of_iterations = 10
real_range = [-5,5]
imag_range = [-5,5]
num_of_points_each_direction = 100

#print(nmif.newtons_method_visuals(f,tol,num_of_iterations,real_range,imag_range,num_of_points_each_direction,roots_graph=1,fractal=1,real_graph=1))

"""
Test 4

High power polynomial
"""

f = lambda z: -16 + 15*z**4 + z**8
tol = 10**(-4)
num_of_iterations = 100
real_range = [-5,5]
imag_range = [-5,5]
num_of_points_each_direction = 100

#print(nmif.newtons_method_visuals(f,tol,num_of_iterations,real_range,imag_range,num_of_points_each_direction,roots_graph=1,fractal=1,real_graph=1))

"""
Test 5

Only the roots of a high power polynomial (no graphs)
"""

f = lambda z: -16 -7*z**2 + 20*z**3 + 15*z**4 + z**8
tol = 10**(-4)
num_of_iterations = 100
real_range = [-5,5]
imag_range = [-5,5]
num_of_points_each_direction = 100

sol = nmif.newtons_method_visuals(f,tol,num_of_iterations,real_range,imag_range,num_of_points_each_direction)
#print(sol)

"""
Test 6

Function where most of the points should not produce an answer
"""

f = lambda z: 1/z + 1
tol = 10**(-4)
num_of_iterations = 100
real_range = [-5,5]
imag_range = [-5,5]
num_of_points_each_direction = 100

#print(nmif.newtons_method_visuals(f,tol,num_of_iterations,real_range,imag_range,num_of_points_each_direction,roots_graph=1,fractal=1,real_graph=1))


"""

Misc Functions for Future Use
"""

f = lambda z: z**5 - 1
tol = 10**(-4)
num_of_iterations = 100
real_range = [-5,5]
imag_range = [-5,5]
num_of_points_each_direction = 100

#print(nmif.newtons_method_visuals(f,tol,num_of_iterations,real_range,imag_range,num_of_points_each_direction,roots_graph=1,fractal=1,real_graph=1))

