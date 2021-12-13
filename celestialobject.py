# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 15:26:10 2020

@author: Arthur
"""
import numpy as np
import random
import string
import tkinter as tk
import math


class Trajectory:
    """
      A class that functionality that can make the celestial object have a certain
            initial velocity wrt a Keplerian trajectory around one or more 
            existing celestial objects.
      Attributes
    ----------                      
    orbited_celestial_objects: array of celestial bodies
      celestial bodies that the trajectory should be around, 
    G: numerical value gravitational constant,
    direction: numerical 
        direction(1 for clockwise, -1 for counterclockwise)]
    eccentricity: numerical
        the eccentricity, e,  of the orbit: 0: circular, 0<e<1: elliptical
        e>1: hyperbolic
    angle: numerical
        angle between the 
            
    
     
    """
    def __init__(self, orbited_celestial_objects, G,
                 direction=1, eccentricity=0, angle=0):
        #make a list if only one celestial object is to be oribted around
        if  not isinstance(orbited_celestial_objects, list):
            self.orbited_celestial_objects = [orbited_celestial_objects]
        else:
            self.orbited_celestial_objects = orbited_celestial_objects
        self.G = G
        self.direction = direction
        self.eccentricity = eccentricity
        self.angle = angle

class Celestialobject():
    """
    A class that represents a Celestial object or body


    Attributes
    ----------
    mass : numerical
        mass of the Celestial object
    color : str
        color for the Celestial object
    canvas : tkinter.Canvas
        Canvas on which the Celestial object is drawn
    position: numpy array
        The  position vector on the canvas
    velocity: numpy array
        The velocity vector
    name: str
        name of the Celestial object
    radius: numerical
        the size on canvas in pixels of the Celestial object
    force: numpy array
        The total force acting on the Celestial object
    acceleration: numpy array
        The  acceleration vector
    speed_history: array
        keeps history of the velocity
    acceleration_history: array
        keeps history of the accelaration
    phi_history
        keeps history of the phic, the angle between the accelaration
        and velocity vectors
    oval: tkinter oval
        The graphical representation of the Celestial object on the Tkinter canvas
    force_arrow: tkinter line
        The graphical representation of the force_arrow
    keep_history = boolean
        keep history of the speed, acceleration and phi?


    """


    def __init__(self, mass:float, color:str, canvas,
                 position:np.array,
                 velocity:np.array=np.zeros((2,)),
                 name:str = '', radius:float = 0):
        """
        Initiates the Celstial Object

        Parameters
        ----------
        mass : numerical
            mass of the Celestial object
        color : str
            color for the Celestial object
        canvas : tkinter.Canvas
            Canvas on which the Celestial object is drawn
        position: numpy array
            The starting  position vector on the canvas
        velocity: numpy array
            The velocity vector
        name: str
            name of the Celestial object
        radius: numerical
            the size on canvas in pixels of the Celestial object
        trajectory: dict 
            If a certain trajectory is 
        Returns
        -------
        None.

        """
        self.mass = mass
        if radius == 0:
            self.radius = max(int(3*math.sqrt(mass)), 1)
        else:
            self.radius = radius
        self.position = np.array(position).astype(np.float64)
        self.canvas_position = self.position
        self.velocity = np.array(velocity).astype(np.float64)
       
        self.force = np.zeros((2,))
        self.acceleration = np.zeros((2,))
        self.color = color
        if name == '':
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(6))
            self.name = 'planet'+result_str
        coords_circle = [position[0]-self.radius/2, position[1]-self.radius/2,
                         position[0]+self.radius/2, position[1]+self.radius/2]
        self.canvas = canvas
        self.oval = canvas.create_oval(
            coords_circle[0], 
            coords_circle[1], 
            coords_circle[2], 
            coords_circle[3], 
            fill=color
            )
        self.force_arrow = canvas.create_line(coords_circle[0], coords_circle[1], coords_circle[2], coords_circle[3], arrow=tk.LAST, fill=self.color)
        self.velocity_arrow = canvas.create_line(coords_circle[0], coords_circle[1], coords_circle[2], coords_circle[3], arrow=tk.LAST, fill=self.color)
        self.keep_history = True
        # self.maxsize
        self.speed_history = []
        self.acceleration_history = []
        self.phi_history = []

    @classmethod
    def fromtrajectory(cls, mass:float, color:str, canvas,
                 position,
                 trajectory:Trajectory,
                 name:str = '', radius:float = 0):
        celestialobject = Celestialobject(mass, color, canvas,
                    position,
                    np.zeros((2,)),
                    name, radius)
        velocity = celestialobject.get_velocity_for_trajectory(trajectory)
        celestialobject.velocity = velocity
        return celestialobject
        

    def reset_force(self):
        """
        Sets the force vector to 0

        Returns
        -------
        None.

        """
        self.force = np.zeros((2,))

    # def update_parameters(self, position. )
    def move_object(self, change, draw_tail=True, color_trail=''):
        """
        Moves the oval representing the Celestial object on the canvas

        Parameters
        ----------
        change : numerical
            How much the Celestial objects should move on the canvas
        draw_tail : Bool, optional
            If the tail should be drawn. The default is True.
        color_trail : TYPE, optional
            Color of the tail. The default is '' which leads to color of the
            Celestial objects.

        Returns
        -------
        None.

        """
        self.canvas.move(self.oval, change[0], change[1])
        self.canvas_position = self.get_center_oval()
        if draw_tail: # and norm(change)>.5:
            if color_trail == '':
                color_trail = self.color
            self.canvas.create_rectangle((self.canvas_position[0], self.canvas_position[1])*2
                                         ,outline=color_trail)

    def get_acceleration(self, correction=np.zeros((2,))):
        return norm(self.acceleration + correction)

    def get_speed(self, correction=np.zeros((2,))):
        return norm(self.velocity + correction)

    def get_center_oval(self):
        coords = self.canvas.coords(self.oval)
        return np.array([(coords[0] + coords[2])/2, (coords[1] + coords[3])/2])

    def get_phi(self):
        return angle_between(self.acceleration, self.velocity)

    def new_state(self, delta_t):
        """


        Parameters
        ----------
        delta_t : numerical
            the time interval between two states.

        Returns
        -------
        None.

        """
        self.acceleration = self.force / self.mass
        self.velocity += self.acceleration*delta_t
        self.position += self.velocity*delta_t
        if self.keep_history:
            self.speed_history.append(self.get_speed())
            self.acceleration_history.append(self.get_acceleration())
            self.phi_history.append(self.get_phi())

    def draw_acceleration_arrow(self, correction=np.zeros((2,)), factor = 160):
        """
        Draws the accelaration vector as an arrow on the screen

        Parameters
        ----------
        correction : numerical, optional
            Correction of the vector in position. The default is np.zeros((2,)).
        factor : numerical, optional
            used to enlarge the vector arrow w.r.t. . The default is 160.. The default is 160.

        Returns
        -------
        None.

        """

        if factor != 0:
            start_point = self.canvas_position
            end_point = start_point + (self.acceleration + correction) * factor
            self.canvas.coords(self.force_arrow,start_point[0], start_point[1], end_point[0], end_point[1])

    def draw_velocity_arrow(self, correction=np.zeros((2,)), factor = 30):
        """
        Draws the velocity vector as an arrow on the screen

        Parameters
        ----------
        correction : numerical, optional
            Correction of the vector in position. The default is np.zeros((2,)).
        factor : numerical, optional
            used to enlarge the vector arrow w.r.t. . The default is 160. The default is 30.

        Returns
        -------
        None.

        """
        if factor != 0:
            start_point = self.canvas_position
            end_point = start_point + (self.velocity + correction) * factor
            self.canvas.coords(self.velocity_arrow,start_point[0], start_point[1], end_point[0], end_point[1])

    def get_velocity_for_trajectory(self, trajectory:Trajectory):
        velocity = np.zeros((2,))
        if trajectory.eccentricity == -1:
            print("Not a possible eccentricty value")
        elif trajectory.eccentricity == 0:
            velocity =  self.get_velocity_circulair_trajectory(trajectory)
        
        else:
            velocity = self.get_velocity_trajectory(trajectory)
        return velocity

    def get_velocity_circulair_trajectory(self, trajectory:Trajectory):
        """
        Calculates the needed velocity for a celestial object to 
        make a circular trajectory around one or more celestial objects.
        The resulting trajectory might be perturbed by the presence of 
        other celestial trajectorys.

        Parameters
        ----------
        trajectoryed_celestial_objects : TYPE
            DESCRIPTION.
        G : numerical
            Gravitational constant G.
        direction : +1,-1
            wether trajectory should be clockwise (1) or counter clockwise (-1).

        Returns
        -------
        v_total : numpy array
            the total speed the celestial object should have to orbit around 
            several celestial objects.

        """
        r_cm, v_cm, m_cm, r = self.get_parameters_trajectory(trajectory)
        theta = math.atan2(r[1], r[0])
        v_trajectory_radial = math.sqrt(
            trajectory.G * m_cm  / norm(r) 
            )
        v_trajectory_cartesian = v_trajectory_radial  * trajectory.direction * np.array([-math.sin(theta), math.cos(theta)])
        v_total = v_trajectory_cartesian  + v_cm
        return v_total
    
    def get_velocity_trajectory(self, trajectory:Trajectory):
        """
        Calculates the required velocity for a celestial object to 
        make a circular trajectory around one or more celestial objects.
        The resulting trajectory might be perturbed by the presence of 
        other celestial trajectorys.

        Parameters
        ----------
        trajectored_celestial_objects : Trajectory
            The trajectory the celestial body will initially set out.

        Returns
        -------
        velocity : numpy array
            the total speed the celestial object should have to orbit around 
            several celestial objects.

        """
        
        r_cm, v_cm, m_cm, r = self.get_parameters_trajectory(trajectory)
        theta = trajectory.angle
        e = trajectory.eccentricity
        alpha = 1 + e * math.cos(theta)
        beta = alpha * norm(r)
        v_factor = trajectory.direction* math.sqrt(
            2 * trajectory.G * m_cm / beta
            )
        v_r = v_factor  * e * math.sin(theta)
        v_theta = v_factor * alpha
        phi = math.atan2(r[1], r[0])
        e_r = np.array([np.cos(phi), np.sin(phi)])
        e_phi = np.array([-np.sin(phi), np.cos(phi)])
        v_vec = v_r * e_r + v_theta * e_phi
        velocity = v_vec + v_cm
        return velocity
    
    def get_parameters_trajectory(self, trajectory:Trajectory):
        r_cm = np.array(
            get_center_of_mass_coordinates(trajectory.orbited_celestial_objects)
            )
        v_cm = np.array(
            get_center_of_mass_velocity(trajectory.orbited_celestial_objects)
            )
        m_cm = sum([planet.mass for planet in trajectory.orbited_celestial_objects])
        r = self.position - r_cm
        return r_cm, v_cm, m_cm, r


        
def set_force_2_celestialobjects(
        celestialobject_1:Celestialobject, celestialobject_2:Celestialobject,
        G, alpha=2
        ):
    """
    Calculates and updates the gravitational forces between two celestial bodies

    Parameters
    ----------
    celestialobject_1 : celestialobject
        DESCRIPTION.
    celestialobject_2 : celestialobject
        DESCRIPTION.
    G : numerical
        DESCRIPTION.
    alpha : TYPE, optional
        DESCRIPTION. The default is 2.

    Returns
    -------
    None.

    """
    distance = celestialobject_2.position - celestialobject_1.position
    F_12 = G * celestialobject_1.mass * celestialobject_2.mass/ (
        norm(distance)**(alpha+1) ) * distance
    celestialobject_1.force = celestialobject_1.force + F_12
    celestialobject_2.force = celestialobject_2.force - F_12
    
def unit_vector(v):
    return v / norm(v)


def angle_between(v, u):
    v = unit_vector(v)
    u = unit_vector(u)
    return np.arccos(np.clip(np.inner(v, u),-1,1))

def norm(v):
    return np.sqrt(np.inner(v, v)) #Faster than np.linalg.norm(x)

def get_center_of_mass_coordinates(celestialobjects):
    return sum([planet.mass*planet.position for planet in celestialobjects]) / sum([planet.mass for planet in celestialobjects])

def get_center_of_mass_velocity(celestialobjects): 
    return sum([planet.mass*planet.velocity for planet in celestialobjects]) / sum([planet.mass for planet in celestialobjects])
