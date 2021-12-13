# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 15:26:10 2020

@author: Arthur
"""
import numpy as np
import random
import string
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

    def __init__(self, mass:float, color:str,
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
            # self.radius = max(2*math.sqrt(mass), 1)
            self.radius = 3*max(mass**(1/3), 1)
        else:
            self.radius = radius
        self.position = np.array(position).astype(np.float64)
        self.velocity = np.array(velocity).astype(np.float64)
        self.force = np.zeros((2,))
        self.acceleration = np.zeros((2,))
        self.color = color
        if name == '':
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(6))
            self.name = 'planet'+result_str
        else:
            self.name = name
        self.keep_history = True
        self.speed_history = []
        self.acceleration_history = []
        self.phi_history = []
        self.tail=[]

    @classmethod
    def fromtrajectory(cls, mass:float, color:str,
                 position,
                 trajectory:Trajectory,
                 name:str = '', radius:float = 0):
        celestialobject = Celestialobject(mass, color,
                    position,
                    np.zeros((2,)),
                    name, radius)
        velocity = celestialobject.get_velocity_for_trajectory(trajectory)
        celestialobject.velocity = velocity
        return celestialobject
    
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
       v_trajectory_cartesian = (
           v_trajectory_radial  * trajectory.direction 
           * np.array([-math.sin(theta), math.cos(theta)])
           )
       v_total = v_cm + v_trajectory_cartesian
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
       sign = trajectory.direction
       alpha = 1 + e * sign * math.cos(theta)
       a = r * alpha / (1-e*e)
       beta = a*(1-e*e)
       v_factor = math.sqrt(2 * trajectory.G * m_cm / beta)
       v_r = v_factor  * e * math.sin(theta)
       v_theta = v_factor * alpha
       coords_2 = self.center+np.array([r,0])
       r_vec = self.center - coords_2
       phi = math.atan2(r_vec[1], r_vec[0])
       e_r = np.array([np.cos(phi), np.sin(phi)])
       e_phi = np.array([-np.sin(phi), np.cos(phi)])
       v_vec = v_r * e_r + v_theta * e_phi
       velocity = v_cm + v_vec
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
    def reset_force(self):
        self.force = np.zeros((2,))

    def update_tail(self, tail_length=1000):
        self.tail.append(np.copy(self.position))
        if len(self.tail) > tail_length:
            del self.tail[0]

    def get_acceleration(self, correction=np.zeros((2,))):
        return norm(self.acceleration + correction)

    def get_speed(self, correction=np.zeros((2,))):
        return norm(self.velocity + correction)


    def get_phi(self):
        return angle_between(self.acceleration, self.velocity)

    def new_state_planet(self, delta_t):
        self.acceleration = self.force / self.mass
        self.velocity += self.acceleration * delta_t
        self.position += self.velocity * delta_t
        if self.keep_history:
            self.speed_history.append(self.get_speed())
            self.acceleration_history.append(self.get_acceleration())
            self.phi_history.append(self.get_phi())

def set_state_after_collision(celestialobject_1, celestialobject_2, r_21, r_21_norm, r_21_in_v_12):
    vector = 2*r_21_in_v_12/((celestialobject_1.mass + celestialobject_2.mass)*r_21_norm**2)*r_21
    celestialobject_1.velocity -= celestialobject_2.mass*vector
    celestialobject_2.velocity += celestialobject_1.mass*vector


def handle_collision(celestialobject_1, celestialobject_2, r_21, r_21_norm, R_12, delta_t, enterIsPossible):
    v_12 = celestialobject_1.velocity - celestialobject_2.velocity
    r_21_in_v_12 = np.dot(r_21, v_12)
    v_12_2 = np.dot(v_12, v_12)
    if not enterIsPossible:
        # calculate time where collision happened
        t_c = (math.sqrt(r_21_in_v_12**2 - v_12_2*(r_21_norm**2 - R_12**2)) - r_21_in_v_12)/ v_12_2
        # Set positions at where the collison happened
        celestialobject_1.position -= t_c * celestialobject_1.velocity
        celestialobject_2.position -= t_c * celestialobject_2.velocity
        r_21 = celestialobject_2.position - celestialobject_1.position
        r_21_norm = norm(r_21)
        r_21_in_v_12 = np.dot(r_21, v_12)
    set_state_after_collision(celestialobject_1, celestialobject_2, r_21, r_21_norm, r_21_in_v_12)


    if not enterIsPossible:
        # Adjust positions to "current time"
        celestialobject_1.position += abs(delta_t - t_c) * celestialobject_1.velocity
        celestialobject_2.position += abs(delta_t - t_c) * celestialobject_2.velocity



def set_forces_2celestialobjects(celestialobject_1, celestialobject_2, G, delta_t, alpha=2, collisionsOn=True, enterIsPossible=False):
    r_21 = celestialobject_2.position - celestialobject_1.position
    r_21_norm = norm(r_21)
    R_12 = celestialobject_1.radius + celestialobject_2.radius
    collison = False
    # collisions
    if collisionsOn and r_21_norm <= R_12:
        collison = True
        handle_collision(celestialobject_1, celestialobject_2, r_21, r_21_norm, R_12, delta_t, enterIsPossible)
        r_21 = celestialobject_2.position - celestialobject_1.position
        r_21_norm = norm(r_21)
    F_12 = G * celestialobject_1.mass * celestialobject_2.mass /  r_21_norm**(alpha+1) * r_21
    celestialobject_1.force = celestialobject_1.force + F_12
    celestialobject_2.force = celestialobject_2.force - F_12
    return collison

def get_coords_com(celestialobjects):
        return sum([planet.mass*planet.position for planet in celestialobjects]) / sum([planet.mass for planet in celestialobjects])

    # def create_reandom_planet(range_mass=[1,20], range_size=[1,20], range_location=[100,800], range_velocity=[-5,5]):
    #     co.celestialobject(9, 8, self.center, [-.05, 0])



def set_new_state(celestialobjects, G, alpha, delta_t, collisionsOn=True, enterIsPossible=False):
    for planet in celestialobjects:
        planet.reset_force()

    if len(celestialobjects) > 1:
        for i, planet1 in enumerate(celestialobjects[:-1]):
            for planet2 in celestialobjects[i+1::]:
                collision = set_forces_2celestialobjects(
                    planet1, planet2, G, delta_t, alpha, collisionsOn, enterIsPossible)

    for planet in celestialobjects:
        planet.new_state_planet(delta_t)

    return collision

def unit_vector(vector):
    return vector / norm(vector)


def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.inner(v1_u, v2_u))

def norm(v):
    return np.sqrt(np.inner(v, v)) #Faster than np.linalg.norm(x)

def get_center_of_mass_coordinates(celestialobjects):
    return (
        sum([planet.mass*planet.position for planet in celestialobjects]) 
        / sum([planet.mass for planet in celestialobjects])
        )

def get_center_of_mass_velocity(celestialobjects): 
    return (
        sum([planet.mass*planet.velocity for planet in celestialobjects]) 
        / sum([planet.mass for planet in celestialobjects])
            )