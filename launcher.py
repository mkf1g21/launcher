#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 09:46:55 2022
@author: michael
"""
import matplotlib.pyplot as plt
import numpy as np


class Launcher:
    # constants
    g = -9.81
    m = 0.024  # https://www.dimensions.com/element/squash-ball
    d = 0.040

    # variables
    u_x = 0
    u_y = 0
    theta = 0  # in radians
    exit_velocity = 0
    c_d = 1
    times = []

    acceleration_distance = 0
    acceleration_force = 10
    exit_angle = 45
    c_f = 0.1

    bungee_length = 0.5
    eta = 0.9

    # TODO: continuous angle with 2 power settings

    """------------------------------trajectory-----------------------------"""

    def get_CD(self, V_mag):
        rho = 1.204    # kg/m^3
        mu = 1.825e-5  # Pa s
        Re = rho * V_mag * self.d / mu
        return (24/Re * (1 + 0.27*Re)**0.43 + 0.47 * (1 - np.exp(-0.04*Re**0.38)))

    def set_components(self, x, y):
        """sets the components of velocity from the x and y components.
        automatically finds the launch angle and speed"""
        self.u_x = x
        self.u_y = y
        self.exit_velocity = (x ** 2 + y ** 2) ** 0.5
        self.theta = np.arctan(y / x)

    def set_angles(self, exit_velocity, theta):
        """sets launch angle and exit velocity. automatically sets the
        components of velocity in x and y"""
        self.exit_velocity = exit_velocity
        self.theta = theta
        self.u_x = exit_velocity * np.cos(theta)
        self.u_y = exit_velocity * np.sin(theta)

    def setExitVelocity(self, force, distance, angle, C_f=0, degrees=True):
        """sets the distance the ball will travel while under acceleration.
        Needs the angle to still work with the rest of
        the code"""
        #TODO change to use coefficient of friction, needs a more complex suvat because of changing a
        v = (2 * (force / self.m) * distance) ** 0.5
        self.exit_velocity = v
        if degrees:
            self.theta = np.radians(angle)
        else:
            self.theta = angle

    def get_time_of_flight(self):
        """returns the time the ball is in the air, assumes start and final
        height are the same"""
        return (2 * self.u_y) / abs(self.g)

    def get_range(self):
        """returns the distance the ball travells in a vaccum"""
        return self.get_time_of_flight() * self.u_x

    def feeg1002_Range(self, mag, theta):
        return -np.sin(2 * theta) * mag ** 2 / self.g 

    def get_range_drag(self, dt=0.001):
        """numerically finds the distance the ball should travel including drag"""
        height = 0
        distance = 0
        v_x = self.u_x
        v_y = self.u_y
        a_x = 0
        a_y = 0
        F_x = 0
        F_y = 0
        vs = []

        rho = 1.225

        area = (0.5 * self.d) ** 2
        while True:
            vs.append(v_x)
            height = height + v_y * dt
            distance = distance + v_x * dt

            a_x = rho * 0.5 * self.get_CD((v_x** 2 + v_y ** 2) ** 0.5) * v_x ** 2 * area * -1
            a_y = (rho * 0.5 * self.get_CD((v_x** 2 + v_y ** 2)** 0.5) * v_y ** 2 * area * -1) + self.g

            v_y = v_y + a_y * dt
            v_x = v_x + a_x * dt
            # print(v_x, v_y, a_x, a_y, height)

            if height <= 0:
                break
        return(distance)
        # plt.plot(vs)

    def plot_angle_v_range(self, dt=0.001):
        """plots the distance the projectile gets to across angles, one with
        and one without drag"""
        angles = np.linspace(0, (np.pi) / 2, num=180)
        dRanges = []
        ranges = []
        feeg1002ranges = [self.feeg1002_Range(self.exit_velocity, theta) for theta in angles]
        for theta in angles:
            self.set_angles(self.exit_velocity, theta)
            dRanges.append(self.get_range_drag(dt))
            ranges.append(self.get_range())
        plt.plot(np.degrees(angles), ranges, label="vaccum")
        plt.plot(np.degrees(angles), dRanges, label="drag at c_d from function")
        plt.plot(np.degrees(angles), feeg1002ranges, label="ranges from dynamics")
        plt.xlabel("tube angle (°)")
        plt.ylabel("distance (m)")
        plt.title
        plt.legend()
        plt.yticks([1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5])
        plt.grid()
        plt.show()

    """------------------------launch mechanism----------------------------"""

    def bow_exit_velocity(cart_disp, arm_length, relaxed_elastic, bungee_const, mtot, eta):
        """
        Compute launch velocity from launcher settings.
        """
    # length of bungee before firing
        stretched_bungee = np.sqrt(arm_length ** 2 + cart_disp ** 2)

        return np.sqrt( (eta * bungee_const * (stretched_bungee-relaxed_elastic)**2 - bungee_const * (arm_length-relaxed_elastic)**2) / mtot )











