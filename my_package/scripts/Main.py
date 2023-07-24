
# import math
from Obstacles import *
from Functions import *

def run_program():

    clearance = float(input("Enter the clearance value in mm, preferably 50\n"))
    radius = 105.0 #radius of turtle bot is 105 mm
    clearance = clearance/1000 #converting to meters
    radius = radius/1000
    d = clearance + radius

    input_start_x = input("Enter start position 'x' coordinate, preferably 1\n") #taking user input for start coordinates; reprompt if in obstacle
    input_start_y = input("Enter start position 'y' coordinate, preferably 1 \n")
    input_start_theta = input("Enter start position's orientation - theta value, preferably 0\n")
    input_start_coordinates = (int(input_start_x), int(input_start_y), int(input_start_theta))
    while obstacle((input_start_coordinates[0], input_start_coordinates[1], d)):
        print("The entered value is in the obstacle. Please enter new values\n")
        input_start_x = input("Enter start position 'x' coordinate, preferably 1\n")
        input_start_y = input("Enter start position 'y' coordinate, preferably 1\n")
        input_start_theta = input("Enter start position's orientation - theta value, preferably 0\n")
        input_start_coordinates = ([int(input_start_x), int(input_start_y), int(input_start_theta)])


    input_goal_x = input("Enter goal position 'x' coordinate, preferably 9\n") #taking user input for goal coordinates; reprompt if in obstacle
    input_goal_y = input("Enter goal position 'y' coordinate,  preferably 9\n")
    input_goal_theta = input("Enter goal position's orientation - theta value, preferably 0\n")
    input_goal_coordinates = (int(input_goal_x), int(input_goal_y), int(input_goal_theta))
    while obstacle((input_goal_coordinates[0], input_goal_coordinates[1], d)):
        print("The entered value is in the obstacle. Please enter new values\n")
        input_goal_x = input("Enter goal position 'x' coordinate, preferably 9\n")
        input_goal_y = input("Enter goal position 'y' coordinate,  preferably 9\n")
        input_goal_theta = input("Enter goal position's orientation - theta value, preferably 0\n")
        input_goal_coordinates = ([int(input_goal_x), int(input_goal_y), int(input_goal_theta)])

    #input wheel RPM
    left_RPM = int(input("Enter left wheel RPM, preferably 50\n"))
    right_RPM = int(input("Enter right wheel RPM, preferably 40\n"))


    # create_map() #create the map to show the obstacles
    solution_travelled_path = A_star(input_start_coordinates, input_goal_coordinates, radius, clearance, left_RPM, right_RPM)
    print(solution_travelled_path)
    # show_path_travelled(solution_travelled_path)
    print("Success")
    return solution_travelled_path

run_program()

# f = open("output.txt", "r+")

# for d in solution_travelled_path:
#     f.write(f"{d}\n")

# f.close()