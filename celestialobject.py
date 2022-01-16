# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 15:26:10 2020

@author: Arthur
"""
import numpy as np
import random
import string
import math
# TODO: Add preset init for objects at vertices of geometric shapes

class Trajectory:
    """
    A class that functionality that can make the celestial object have a 
    certain initial velocity wrt a Keplerian trajectory around one or more
    existing celestial objects.
    
    Attributes
    ----------                      
        orbited_celestial_objects: List of the Celestial objects
        which the new Celestial orbit will initially orbit. 
        G: numerical value gravitational constant,
        direction: numerical 
            direction(1 for clockwise, -1 for counterclockwise)]
        eccentricity: numerical
            the eccentricity, e,  of the orbit: 0: circular, 0<e<1: elliptical
            e>1: hyperbolic
        angle: numerical
            angle between the orbeting celestial objct and the semi-major axis of 
            the trajectory
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
        keep_history = boolean
            keep history of the speed, acceleration and phi
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
       position: numpy array
           The starting  position vector on the canvas
       velocity: numpy array
           The velocity vector
       name: str
           name of the Celestial object
       radius: numerical
           the size on canvas in pixels of the Celestial object
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
        self.tail = []

    @classmethod
    def fromtrajectory(cls, mass:float, color:str,
                 position,
                 trajectory:Trajectory,
                 name:str = '', radius:float = 0):
        """
        A factory method to iniate a Celestial object using a trajectory around
        one or more Celestial objects

        Parameters
        ----------
        cls : TYPE
            DESCRIPTION.
        mass : numerical
            mass of the Celestial object
        color : str
            color for the Celestial object
        position: numpy array
            The starting  position vector on the canvas
        name: str
            name of the Celestial object
        radius: numerical
            the size of the Celestial object on the screen in pixels 

        Returns
        -------
        celestialobject : Celestialobject
    

        """
        celestialobject = Celestialobject(mass, color,
                    position,
                    np.zeros((2,)),
                    name, radius)
        velocity = celestialobject.get_velocity_for_trajectory(trajectory)
        celestialobject.velocity = velocity
        return celestialobject
    
    def get_velocity_for_trajectory(self, trajectory:Trajectory):
        velocity = np.zeros((2,))
        if trajectory.eccentricity == -1:
            print("Not a possible eccentricty value")
        elif trajectory.eccentricity == 0:
            velocity =  self.get_velocity_circulair_trajectory(trajectory)
        else:
            velocity = self.get_velocity_noncircular_trajectory(trajectory)
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
       v_trajectory_cartesian = (
           v_trajectory_radial  * trajectory.direction 
           * np.array([-math.sin(theta), math.cos(theta)])
           )
       v_total = v_cm + v_trajectory_cartesian
       return v_total
   
    def get_velocity_noncircular_trajectory(self, trajectory:Trajectory):
       """
       Calculates the required velocity for a celestial object to 
       make a circular trajectory around one or more celestial objects.
       The resulting trajectory might be perturbed by the presence of 
       other celestial trajectorys.
       Parameters
       ----------
       trajectory : Trajectory
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
       velocity = v_cm + v_vec
       return velocity
   
    def get_parameters_trajectory(self, trajectory:Trajectory):
        """
        Calculates important parameters need to for calculations in the trajectory

        Parameters
        ----------
        trajectory : Trajectory
            DESCRIPTION.

        Returns
        -------
        r_cm : numpy array
        The postition vector of the center of mass of the Celestial objects
        which the new Celestial orbit will -initially - orbit.
        v_cm : numpy array
            DESCRIPTION.
        m_cm : numerical
            Th.
        r : numerical
            DESCRIPTION.

        """
        poistion_center_of_mass = np.array(
            get_center_of_mass_coordinates(trajectory.orbited_celestial_objects)
            )
        velocity_center_of_mass = np.array(
            get_center_of_mass_velocity(trajectory.orbited_celestial_objects)
            )
        mass_orbited_celestial_objects = sum(
            [planet.mass for planet in trajectory.orbited_celestial_objects]
            )
        positiondiff_coobject_com = self.position - poistion_center_of_mass
        return (poistion_center_of_mass, velocity_center_of_mass,
    mass_orbited_celestial_objects, positiondiff_coobject_com )
    
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
        """
        Calculates and sets the vector quantities of the new future state of a 
        Celestial object 

        Parameters
        ----------
        delta_t : nummerical
            time interval between current state and next state.

        Returns
        -------
        None.

        """
        self.acceleration = self.force / self.mass
        self.velocity += self.acceleration * delta_t
        self.position += self.velocity * delta_t
        if self.keep_history:
            self.speed_history.append(self.get_speed())
            self.acceleration_history.append(self.get_acceleration())
            self.phi_history.append(self.get_phi())

def substract_centerofmass_velocity(celestialobjects):
    v_cm = get_center_of_mass_velocity(celestialobjects)
    for celestialobject in celestialobjects:
        celestialobject.velocity -= v_cm

def set_forces_2celestialobjects(
        celestialobject_1:Celestialobject, 
        celestialobject_2:Celestialobject,
        G, delta_t, alpha=2, 
        collisionsOn=True, 
        enterIsPossible=False):
    r_21 = celestialobject_2.position - celestialobject_1.position
    r_21_norm = norm(r_21)
    R_12 = celestialobject_1.radius + celestialobject_2.radius
    collison = False
    # collisions
    if collisionsOn and r_21_norm <= R_12:
        collison = True
        handle_collision(celestialobject_1, 
                         celestialobject_2, 
                         r_21, r_21_norm, R_12, 
                         delta_t, enterIsPossible)
        r_21 = celestialobject_2.position - celestialobject_1.position
        r_21_norm = norm(r_21)
    F_12 = G * celestialobject_1.mass * celestialobject_2.mass /  r_21_norm**(alpha+1) * r_21
    celestialobject_1.force = celestialobject_1.force + F_12
    celestialobject_2.force = celestialobject_2.force - F_12
    return collison

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

def set_state_after_collision(
        celestialobject_1:Celestialobject, 
        celestialobject_2:Celestialobject, 
        r_21, 
        r_21_norm, 
        r_21_in_v_12):
    """

    Parameters
    ----------
    celestialobject_1 : Celestialobject
        DESCRIPTION.
    celestialobject_2 : Celestialobject
        DESCRIPTION.
    r_21 : TYPE
        DESCRIPTION.
    r_21_norm : TYPE
        DESCRIPTION.
    r_21_in_v_12 : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    vector = 2*r_21_in_v_12/(
        (celestialobject_1.mass + celestialobject_2.mass) * r_21_norm**2
        ) * r_21
    celestialobject_1.velocity -= celestialobject_2.mass*vector
    celestialobject_2.velocity += celestialobject_1.mass*vector

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
        sum([planet.mass * planet.position for planet in celestialobjects]) 
        / sum([planet.mass for planet in celestialobjects])
        )

def get_center_of_mass_velocity(celestialobjects): 
    return (
        sum([planet.mass*planet.velocity for planet in celestialobjects]) 
        / sum([planet.mass for planet in celestialobjects])
            )

def create_celestial_objects_in_geometric_shape(center,
                                                length,
                                                velocity_perpundicular,
                                                n_sides,
                                                mass,
                                                color):
    celestial_objects = []
    delta_angle = 2 * math.pi / n_sides
    for i in range(n_sides):
        angle = i * delta_angle
        position = center + length * np.array(
            [math.cos(angle), math.sin(angle)])
        velocity = velocity_perpundicular * np.array(
            [-math.sin(angle), math.cos(angle)]) 
        celestial_object = Celestialobject(
            mass,
            color,
            position,
            velocity,
            'celestial_object1'
            )
        celestial_objects.append(celestial_object)
    return celestial_objects
        
    