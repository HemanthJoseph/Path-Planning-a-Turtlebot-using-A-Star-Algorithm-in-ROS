
import math
# import matplotlib.pyplot as plt
from collections import deque
import matplotlib.patches as patches
from Obstacles import *

# plt.ion()

th = 15 #theta angle increments in each iteration

def rounding(x, y, th, theta):  #function to perform rounding of values
    x = (round(x * 10) / 10)
    y = (round(y * 10) / 10)
    th = (round(th / theta) * theta)
    return (x, y, th)


def action_set(RPM1, RPM2): #function to generate new action set
    actions = [[RPM1, 0], [0, RPM1], [RPM1, RPM1], [0, RPM2], [RPM2, 0], [RPM2, RPM2], [RPM1, RPM2], [RPM2, RPM1]]
    return actions


def cost(Xi, Yi, Thetai, RPM_L, RPM_R): #function for cost provided
    Thetai = Thetai % 360
    t = 0
    r = 0.038
    L = 0.354
    dt = 0.1
    Xn = Xi
    Yn = Yi
    Thetan = 3.14 * Thetai / 180
    
    # Xi, Yi,Thetai: Input point's coordinates
    # Xs, Ys: Start point coordinates for plot function
    # Xn, Yn, Thetan: End point coordintes

    D = 0
    while t < 1:
        t = t + dt
        Xs = Xn
        Ys = Yn
        Xn += 0.5 * r * (RPM_L + RPM_R) * math.cos(Thetan) * dt
        Yn += 0.5 * r * (RPM_L + RPM_R) * math.sin(Thetan) * dt
        Thetan += (r / L) * (RPM_R - RPM_L) * dt
        D = D + math.sqrt(math.pow((0.5 * r * (RPM_L + RPM_R) * math.cos(Thetan) * dt), 2) + math.pow((0.5 * r * (RPM_L + RPM_R) * math.sin(Thetan) * dt), 2))
    Thetan = 180 * (Thetan) / 3.14
    # UL = (2 * np.pi * RPM_L) / 60
    # UR = (2 * np.pi * RPM_R) / 60
    cost_return = (*rounding(Xn, Yn, Thetan, th), D, RPM_L, RPM_R)
    return cost_return


def valid_child_nodes(current_node, radius, clearance, left_RPM, right_RPM):  #function to check which generated child nodes are valid, not in obstacle
    for action in action_set(left_RPM, right_RPM):
        x, y, theta, cost_, UL, UR = cost(*current_node, *action) #using the cost file provided to calculate values of each child node
        
        #checking if points are in obstacle or not
        d = radius + clearance
        coordinates = (current_node[0], current_node[1], d) #original
        if not obstacle((x, y, d)):
            # plt.plot([current_node[0],x ], [current_node[1], y], color="red", alpha=0.2)
            # plt.pause(0.01)
            yield x, y, theta,cost_, UL, UR

# def create_map():  #function to create the map
#     figure, axes = plt.subplots()
#     axes.set(xlim=(0, 10), ylim=(0, 10))

#     circle_1 = plt.Circle((2, 2), 1, fill='True')
#     circle_2 = plt.Circle((2, 8), 1, fill='True')

#     square_1 = patches.Rectangle((0.25, 4.25), 1.5, 1.5, color='blue')
#     rectangle_1 = patches.Rectangle((3.75, 4.25), 2.5, 1.5, color='blue')
#     rectangle_2 = patches.Rectangle((7.25, 2), 1, 2, color='blue')

#     axes.set_aspect('equal')
#     axes.add_artist(circle_1)
#     axes.add_artist(circle_2)
#     axes.add_patch(square_1)
#     axes.add_patch(rectangle_1)
#     axes.add_patch(rectangle_2)
#     plt.show()

# def show_path_travelled(path):  #function to show the trajectory

#     start_node = path[0]
#     goal_node = path[-1]
#     plt.plot(start_node [0], start_node[1], "Dg")
#     plt.plot(goal_node[0], goal_node[1], "Dg")

#     for i, (x, y, theta) in enumerate(path[:-1]):
#         n_x, n_y, theta = path[i+1]
#         plt.plot([x, n_x], [y, n_y], color="black")

#     plt.show()
#     plt.savefig("Map.png")
#     plt.pause(5)
#     plt.close('all')

def backtrack(goal_node, start_node, travelled_paths): #function to perform backtracking
    current_node_path = goal_node
    path = [goal_node]
    while current_node_path != start_node:
        current_node_path = travelled_paths[current_node_path]
        path.append(current_node_path)
    return path[::-1]

def A_star(start_node, goal_node, radius, clearance, left_RPM, right_RPM): #A star algorithm
    travelled_paths = {}
    open_list = deque()
    visited_list = {} #to keep track of all nodes that have been visited
    initial_cost_to_go = float('inf') #giving initial cost as infinity (an higher bounded value)
    initial_cost_to_come = 0
    open_list.append((start_node, initial_cost_to_go, initial_cost_to_come)) #adding start node to open list, 0 indicates not visited
    while len(open_list) != 0:
        current_node, dist, cost_to_come = open_list.popleft() #cost to go is taken as distance to goal node
        visited_list[(current_node[0], current_node[1])] = 1 #assign this coordinate as visited
        if dist <= 0.5: # goal is in 0.5 vicinity to goal node we assume goal is reached
            goal_node = current_node #if true current node is goal node and break code
            solution_path = backtrack(goal_node, start_node, travelled_paths) #backtracking
            return solution_path
            
        child_nodes = set(valid_child_nodes(current_node, radius, clearance, left_RPM, right_RPM)) #finding all valid children of current node
        for n_x, n_y, n_theta, n_cost, UL, UR in child_nodes:
            dist = math.dist((n_x, n_y), goal_node[:2]) #calculate euclidean distance from current node (child) to goal node
            if visited_list.get((n_x, n_y)) == 1: #if child node is already visited go to next child
                continue
            new_cost = cost_to_come + n_cost #calculating new cost
            for i, item in enumerate(open_list):
                if item[1] + item[2] > new_cost + dist: #if cost of item in open list is higher than new total cost
                    open_list.insert(i,((n_x, n_y, n_theta), dist, new_cost)) #add the new node at the position i in the open list
                    break
            else:
                open_list.append(((n_x, n_y, n_theta), dist, new_cost)) #add the new node at the end of the open list
            travelled_paths[(n_x, n_y, n_theta)] = current_node #add current node to the  travelled path dictionary