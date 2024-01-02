# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 13:58:05 2020

@author: hemna
"""
# -*- coding: utf-8 -*-
# Problem Set 3: Simulating robots
# Name:Hem N Chaudhary
# Collaborators (discussion):None
# Time:a couple of days

import math
import random
import matplotlib
#matplotlib.use("TkAgg")

from ps3_visualize import *
import pylab

# === Provided class Position, do NOT change
class Position(object):
    """
    A Position represents a location in a two-dimensional room, where
    coordinates are given by floats (x, y).
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_new_position(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.get_x(), self.get_y()

        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))

        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y

        return Position(new_x, new_y)

    def __str__(self):
        return "Position: " + str(math.floor(self.x)) + ", " + str(math.floor(self.y))

# === Problem 1
class StandardRoom(object):
    """
    A StandardRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. Each tile
    has some fixed amount of dirt. The tile is considered clean only when the amount
    of dirt on this tile is 0.
    """
    def __init__(self, width, height, dirt_amount):
        """
        Initializes a rectangular room with the specified width, height, and
        dirt_amount on each tile.

        width: an integer > 0
        height: an integer > 0
        dirt_amount: an integer >= 0
        """
        self.width=width
        self.height=height
        
        self.tiles={}  #dictionary for tiles
        for i in range(width):
            for j in range(height):
                self.tiles[(i,j)]=dirt_amount #each tile has dirt_amount=dirt
                

    def get_dirt_amount(self, w, h):
        """
        Return the amount of dirt on the tile (w, h)

        Assumes that (w, h) represents a valid tile inside the room.

        w: an integer
        h: an integer

        Returns: a float
        """
        return float(self.tiles[(w,h)]) #dictonary value of key (w,h)

    def clean_tile_at_position(self, pos, capacity):
        """
        Mark the tile under the position pos as cleaned by capacity amount of dirt.

        Assumes that pos represents a valid position inside this room.

        pos: a Position object
        capacity: a float, the amount of dirt to be cleaned in a single time-step.
                  Can be negative which would mean adding dirt to the tile.

        Note: The amount of dirt on each tile should be NON-NEGATIVE.
              If the capacity exceeds the amount of dirt on the tile, mark it as 0.
        """
        x=math.floor(pos.get_x())
        y=math.floor(pos.get_y())
        if self.tiles[(x,y)]>capacity: #check if dirt>capacity
            self.tiles[(x,y)]=self.tiles[(x,y)]-capacity
        else:                           #dirt<capacity
            self.tiles[(x,y)]=0

    def is_tile_cleaned(self, w, h):
        """
        Return True if the tile (w, h) has been cleaned.

        Assumes that (w, h) represents a valid tile inside the room.

        w: an integer
        h: an integer

        Returns: True if the tile (w, h) is cleaned, False otherwise

        Note: The tile is considered clean only when the amount of dirt on this
              tile is 0.
        """
        if self.tiles[w,h]==0:   #if dirt_amount=0
            return True
        else:
            return False

    def get_num_cleaned_tiles(self):
        """
        Returns: an integer; the total number of clean tiles in the room
        """
        total=0
        for tile in self.tiles.keys(): #all the tiles with dirt_amount=0
            if self.tiles[tile]==0:
                total+=1
                
        return total
       
                

    def is_position_in_room(self, pos):
        """
        Determines if pos is inside the room.

        pos: a Position object.
        Returns: True if pos is in the room, False otherwise.
        """
        x=math.floor(pos.get_x())
        y=math.floor(pos.get_y())
        
        if (x,y) in self.tiles: #check if (x,y) in the key of dictionary
            return True
        else:
            return False

    def get_num_tiles(self):
        """
        Returns: an integer; the total number of tiles in the room
        """
        return self.width*self.height  #definition

    def get_random_position(self):
        """
        Returns: a Position object; a random position inside the room
        """
        x=random.random()*self.width
        y=random.random()*self.height
        
        obj_position=Position(x,y) #create position using position class
        return obj_position


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times, the robot has a particular position and direction in the room.
    The robot also has a fixed speed and a fixed cleaning capacity.

    Subclasses of Robot should provide movement strategies by implementing
    update_position_and_clean, which simulates a single time-step.
    """
    def __init__(self, room, speed, capacity):
        """
        Initializes a Robot with the given speed and given cleaning capacity in the
        specified room. The robot initially has a random direction and a random
        position in the room.

        room:  a StandardRoom object.
        speed: a positive float.
        capacity: a positive float; the amount of dirt cleaned by the robot
                  in a single time-step.
        """
        self.room=room
        self.speed=speed
        self.capacity=capacity
        self.position=self.room.get_random_position() #create random room using position attribute
        self.direction=random.random()*360

    def get_position(self):
        """
        Returns: a Position object giving the robot's position in the room.
        """
        
        return self.position

    def get_direction(self):
        """
        Returns: a float d giving the direction of the robot as an angle in
        degrees, 0.0 <= d < 360.0.
        """
        return self.direction

    def set_position(self, position):
        """
        Set the position of the robot to position.

        position: a Position object.
        """
        self.position=position

    def set_direction(self, direction):
        """
        Set the direction of the robot to direction.

        direction: float representing an angle in degrees
        """
        self.direction=direction

    def update_position_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Moves robot to new position and cleans tile according to robot movement
        rules.
        """
        # do not change -- implement in subclasses
        raise NotImplementedError

# === Problem 2
class BasicRobot(Robot):
    """
    A BasicRobot is a Robot with the standard movement strategy.

    At each time-step, a BasicRobot attempts to move in its current
    direction; when it would hit a wall, it *instead*
    chooses a new direction randomly.
    """
    def update_position_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Calculate the next position for the robot.

        If that position is valid, move the robot to that position. Mark the
        tile it is on as having been cleaned by capacity amount.

        If the new position is invalid, do not move or clean the tile, but
        rotate once to a random new direction.
        """
        newposition= self.get_position().get_new_position(self.get_direction(), self.speed)  #create new position using the attribute of position class
        
        if not self.room.is_position_in_room(newposition): #check if new positon not in the room
            direction=random.random()*360  
            self.set_direction(direction) #set random direction
        else:   
            self.set_position(newposition) #go to the position
            self.room.clean_tile_at_position(self.get_position(), self.capacity) #clean the position
            
            
            
        
        
        
        


# Uncomment this line to see your implementation of BasicRobot in action!
#test_robot_movement(BasicRobot, StandardRoom)

# === Problem 3
class MalfunctioningRobot(Robot):
    """
    A MalfunctioningRobot is a robot that may accidentally dirty a tile. A MalfunctioningRobot will
    drop some dirt on the tile it's on and pick a new, random direction for itself
    with probability p. If the robot does drop dirt, the amount of dropped dirt should be a
    decimal value between 0 and 0.5. Afterwards, the robot will behave exactly like the BasicRobot
    by attempting to move to a new tile and clean it.
    """
    p = 0.05

    @staticmethod
    def set_dirt_probability(prob):
        """
        Sets the probability of the robot accidentally dirtying the tile equal to prob.

        prob: a float (0 <= prob <= 1)
        """
        MalfunctioningRobot.p = prob

    def dropping_dirt(self):
        """
        Answers the question: Does the robot accidentally drop dirt on the tile
        at this timestep?
        The robot drops dirt with probability p.

        returns: True if the robot drops dirt on its tile, False otherwise.
        """
        return random.random() < MalfunctioningRobot.p

    def update_position_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Check if the robot accidentally releases dirt. If so, dirty the current tile
        by a random decimal value between 0 (inclusive) and 0.5 (exclusive) and change
        its direction randomly.

        Calculate the next position for the robot regardless if the robot releases dirt or not.

        If that position is valid, move the robot to that position. Mark the tile it moved to
        as having been cleaned by capacity amount.

        If it is not a valid position, the robot should change to a random direction.

        """
        if self.dropping_dirt():   #if the dirt was dropped
            dirt=-random.random()*0.5  
            pos=self.get_position()
            self.room.clean_tile_at_position(pos, dirt) #use clean function to drop dirt
            self.set_direction(random.random()*360) #random direction
            
            
        newposition= self.get_position().get_new_position(self.get_direction(), self.speed) #choose new position using position class atribute
        
        if not self.room.is_position_in_room(newposition): #newpositoon not in the room; choose random direction
            direction=random.random()*360
            self.set_direction(direction)
            
            
        else:          #if new position in the room, go to the position and clean the position
            self.set_position(newposition)
            self.room.clean_tile_at_position(self.get_position(), self.capacity)
            
            
            
            
            

# Uncomment this line to see your implementation of MalfunctioningRobot in action!
#test_robot_movement(MalfunctioningRobot, StandardRoom)


# === Problem 4
class SuperRobot(Robot):
    """
    A SuperRobot is a robot that moves extra fast and can clean two tiles in one
    timestep.

    It moves in its current direction, cleans the tile it lands on, and continues
    moving in that direction and cleans the second tile it lands on, all in one
    unit of time.

    If the SuperRobot hits a wall when it attempts to move in its current direction,
    it may dirty the current tile by one unit because it moves very fast and can
    knock dust off of the wall.

    """
    p = 0.15

    @staticmethod
    def set_dirty_probability(prob):
        """
        Sets the probability of getting the tile dirty equal to PROB.

        prob: a float (0 <= prob <= 1)
        """
        SuperRobot.p = prob

    def dropping_dirt(self):
        """
        Answers the question: Does the robot accidentally drop dirt on the tile
        at this timestep?
        The robot drops dirt with probability p.

        returns: True if the robot drops dirt on its tile, False otherwise.
        """
        return random.random() < SuperRobot.p

    def update_position_and_clean(self):
        """
        Simulates the passage of a single time-step.

        Within one time step (i.e. one call to update_position_and_clean), there are
        three possible cases:

        1. The next position in the current direction at the robot's given speed is
           not a valid position in the room, so the robot stays at its current position
           without cleaning the tile. The robot then turns to a random direction.

        2. The robot successfully moves forward one position in the current direction
           at its given speed. Let's call this Position A. The robot cleans Position A.
           The next position in the current direction is not a valid position in the
           room, so it does not move to the new location. With probability p, it dirties
           Position A by capacity 1. Regardless of whether or not the robot dirties Position A,
           the robot will turn to a random direction.

        3. The robot successfully moves forward two positions in the current direction
           at its given speed. It cleans each position that it lands on.
        """
        
        newposition= self.get_position().get_new_position(self.get_direction(), self.speed) #create new position using position class
       #case1 begins near the wall
        if not self.room.is_position_in_room(newposition): #hits the wall
            direction=random.random()*360
            self.set_direction(direction) #choose random direction
        else:  
            #case2 #new position inside the room, go to new position, and clean it
            self.set_position(newposition)
            self.room.clean_tile_at_position(self.get_position(), self.capacity) 
            #case3
            newposition= self.get_position().get_new_position(self.get_direction(), self.speed)  #create new position again
            if not self.room.is_position_in_room(newposition): #hits the wall at the velocity, drops dirt
                if self.dropping_dirt():
                    dirt=-1
                    pos=self.get_position()
                    self.room.clean_tile_at_position(pos, dirt) #use clean attribute to add dirt in the room
                    self.set_direction(random.random()*360)
                else:
                    self.set_direction(random.random()*360)
            else:      # new position still in the room, go to the position, and clean it
            
                self.set_position(newposition)
                
                self.room.clean_tile_at_position(self.get_position(), self.capacity)         
        
        
        
            
        
        

# Uncomment this line to see your implementation of SuperRobot in action!
#test_robot_movement(SuperRobot, StandardRoom)

# === Problem 5
def run_simulation(num_robots, speed, capacity, width, height, dirt_amount, min_coverage, num_trials,
                  robot_type):
    """
    Runs num_trials trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction min_coverage of the room.

    The simulation is run with num_robots robots of type robot_type, each
    with the input speed and capacity in a room of dimensions width x height
    with the dirt dirt_amount on each tile. Each trial is run in its own StandardRoom
    with its own robots.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    capacity: a float (capacity > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    dirt_amount: an int
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. BasicRobot or
                MalfunctioningRobot)
    """
    count=0
    for trials in range(num_trials): #for each trial, creat a room and add num_robots
        robot_list=[]
        room=StandardRoom(width,height,dirt_amount)
        for i in range(num_robots):
            nameR=robot_type(room, speed, capacity)
            robot_list.append(nameR) #keep track of the types and num of robots
            
        while not room.get_num_cleaned_tiles()/room.get_num_tiles()-min_coverage>=0: #unitl min_coverage met, keep cleaning and keep track of the num of times(count)
            for robot in robot_list:
                robot.update_position_and_clean()
            count+=1
    
    return count/num_trials #average time taken to reach min_coverage
                
                
            
    


#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 5, 5, 3, 1.0, 50, BasicRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.8, 50, BasicRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 10, 10, 3, 0.9, 50, BasicRobot)))
#print ('avg time steps: ' + str(run_simulation(1, 1.0, 1, 20, 20, 3, 0.5, 50, BasicRobot)))
#print ('avg time steps: ' + str(run_simulation(3, 1.0, 1, 20, 20, 3, 0.5, 50, BasicRobot)))

# === Problem 6
#
# ANSWER THE FOLLOWING QUESTIONS:
#
# 1)How does the performance of the three robot types compare when cleaning 80%
#       of a 20x20 room?
#SuperRobot is the most efficient robot at cleaning. Basic robot and the MalfunctioningRobot are similar however BasicRobot is slightly better.
#
# 2) How does the performance of the three robot types compare when two of each
#       robot cleans 80% of rooms with dimensions
#       10x30, 20x15, 25x12, and 50x6?
# Similar to question1, SuperRobot is the best for all different kinds of room. Similarly, next best is BasicRobot and the the worst is the MalfunctioningRobot. 
#
#

def show_plot_compare_strategies(title, x_label, y_label):
    """
    Produces a plot comparing the three robot strategies in a 20x20 room with 80%
    minimum coverage.
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    times3 = []
    for num_robots in num_robot_range:
        print ("Plotting", num_robots, "robots...")
        times1.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, BasicRobot))
        times2.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, MalfunctioningRobot))
        times3.append(run_simulation(num_robots, 1.0, 1, 20, 20, 3, 0.8, 20, SuperRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.plot(num_robot_range, times3)
    pylab.title(title)
    pylab.legend(('BasicRobot', 'MalfunctioningRobot', 'SuperRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

def show_plot_room_shape(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    times3 = []
    for width in [10, 20, 25, 50]:
        height = int(300/width)
        print ("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, BasicRobot))
        times2.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, MalfunctioningRobot))
        times3.append(run_simulation(2, 1.0, 1, width, height, 3, 0.8, 200, SuperRobot))
    pylab.plot(aspect_ratios, times1, 'o-')
    pylab.plot(aspect_ratios, times2, 'o-')
    pylab.plot(aspect_ratios, times3, 'o-')
    pylab.title(title)
    pylab.legend(('BasicRobot', 'MalfunctioningRobot', 'SuperRobot'), fancybox=True, framealpha=0.5)
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


show_plot_compare_strategies('Time to clean 80% of a 20x20 room, for various numbers of robots','Number of robots','Time (steps)')
show_plot_room_shape('Time to clean 80% of a 300-tile room for various room shapes','Aspect Ratio', 'Time (steps)')
