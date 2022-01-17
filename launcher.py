#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 09:46:55 2022

@author: michael
"""
import matplotlib.pyplot as plt
import numpy as np


class Launcher:
    #constants
    g = -9.81
    m = 0.024 # https://www.dimensions.com/element/squash-ball
    
    #variables
    u_x = 0
    u_y = 0
    theta = 0 # in radians
    r = 0
    times = []
    

    def set_components(self, x, y):
        """sets the components of velocity from the x and y components.
        automatically finds the launch angle and speed"""
        self.u_x = x
        self.u_y = y
        self.r = (x ** 2 + y ** 2) ** 0.5
        self.theta = np.arctan(y/x)


    def set_angles(self, r, theta):
        """sets launch angle and exit velocity. automatically sets the
        components of velocity in x and y"""
        self.r = r
        self.theta = theta
        self.u_x = r * np.cos(theta)
        self.u_y = r * np.sin(theta)


    def setExitVelocity(force, distance, angle, C_f = 0, degrees = True):
        """sets the distance the ball will travel while under acceleration.
        Needs the angle to still work with the rest of
        the code"""
        #TODO change to use coefficient of friction, needs a more complex suvat because of changing a
        v = (2 * (force/self.m)* distance) ** 0.5
        self.r = v
        if degrees:
            self.theta = np.radians(angle)
        else:
            self.theta = angle


    def get_time_of_flight(self):
        """returns the time the ball is in the air, assumes start and final
        height are the same"""
        return (2 * self.u_y) / abs(self.g)
    
    
    def get_range(self):
        """returns the distance the ball travells"""
        return self.get_time_of_flight() * self.u_x


    def plot_angle_v_range(self):
        angles = np.linspace (0, (np.pi) / 2)
        ranges = []
        for theta in angles:
            self.set_angles(self.r, theta)
            ranges.append(self.get_range())
        plt.plot(np.degrees(angles), ranges)
        plt.show()
