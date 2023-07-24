
import numpy as np
# import matplotlib.pyplot as plt

#Obstacle definition
def circle_obstacle_1(coordinates): #obstacle 1
    x = coordinates[0]
    y = coordinates[1]
    d = coordinates[2]
    if  (((x-2)**2)+((y-2)**2)-((1+d)**2)) <= 0:
        return True
    else:
        return False

def square_obstacle_1(coordinates): #obstacle 2
    x = coordinates[0]
    y = coordinates[1]
    d = coordinates[2]
    if x-(0.25-d) >= 0 and x-(1.75+d) <= 0 and y-(4.25-d) >= 0 and y-(5.75+d) <= 0:
        return True
    else:
        return False

def circle_obstacle_2(coordinates): #obstacle 3
    x = coordinates[0]
    y = coordinates[1]
    d = coordinates[2]
    if  (((x-2)**2)+((y-8)**2)-((1+d)**2)) <= 0:
        return True
    else:
        return False

def rectangle_obstacle_1(coordinates): #obstacle 4
    x = coordinates[0]
    y = coordinates[1]
    d = coordinates[2]
    if x-(3.75-d) >= 0 and x-(6.25+d) <= 0 and y-(4.25-d) >= 0 and y-(5.75+d) <= 0:
        return True
    else:
        return False

def rectangle_obstacle_2(coordinates): #obstacle 5
    x = coordinates[0]
    y = coordinates[1]
    d = coordinates[2]
    if x-(7.25-d) >= 0 and x-(8.75+d) <= 0 and y-(2-d) >= 0 and y-(4+d) <= 0:
        return True
    else:
        return False

def outer_boundary(coordinates): #definition of boundary as an obstacle
    x = coordinates[0]
    y = coordinates[1]
    d = coordinates[2]
    if (x - d <= 0) or (x + d >= 10) or (y - d <= 0) or (y + d >= 10):
        return True
    else:
        return False
    
def obstacle(coordinates): #checking all obstacles + boundaries
    if (outer_boundary(coordinates) or circle_obstacle_1(coordinates) or square_obstacle_1(coordinates) or circle_obstacle_2(coordinates) or rectangle_obstacle_1(coordinates) or rectangle_obstacle_2(coordinates)) == True:
        return True
    else:
        return False

def finalmap(d):
    d  *= 100
    #Background
    # Geometrical definition of the obstacle space
    obstaclespace = np.zeros(shape=(int(1001), int(1001))) 
    # Defining the boundary
    boundary_x = []
    boundary_y = []

    for i in range(1001):
        boundary_x.append(i)
        boundary_y.append(0)
        obstaclespace[0][i] = -1

        boundary_x.append(i)
        boundary_y.append(1000)
        obstaclespace[1000][i] = -1

    for i in range(1001):
        boundary_x.append(0)
        boundary_y.append(i)
        obstaclespace[i][0] = -1

        boundary_x.append(1000)
        boundary_y.append(i)
        obstaclespace[i][1000] = -1
    # plt.scatter(boundary_x, boundary_y, color='g')

# Object 1 = circle_obstacle_1
    circle = []
    for x in range(1001):
        for y in range(1001):
            if (((x-200)**2)+((y-200)**2)-((100+d)**2)) <= 0:
                circle.append((x, y))

    circle_x = [x[0] for x in circle]
    circle_y = [x[1] for x in circle]
    # plt.scatter(circle_x, circle_y, color='b')
    for i in circle:
        obstaclespace[i[1]][i[0]] = -1


# Object 2 = square_obstacle_1
    sideA = []
    sideB = []
    sideC = []
    sideD = []
    for x in range(1001):
        for y in range(1001):
            if x-(0.25*100-d) >= 0:
                sideA.append((x, y))
            if x-(1.75*100+d) <= 0:
                sideB.append((x, y))
            if y-(4.25*100-d) >= 0:
                sideC.append((x, y))
            if y-(5.75*100+d) <= 0:
                sideD.append((x, y))
           
    square1sides = list(set(sideA) & set(sideB) & set(sideC) & set(sideD))
    for i in square1sides:
        obstaclespace[i[1]][i[0]] = -1
    x_square1 = [x[0] for x in square1sides]
    y_square1 = [x[1] for x in square1sides]
    # plt.scatter(x_square1, y_square1, color='b')


# Object 3 = circle_obstacle_2
    circle2 = []
    for x in range(1001):
        for y in range(1001):
            if (((x-200)**2)+((y-800)**2)-((100+d)**2)) <= 0:
                circle2.append((x, y))

    circle2_x = [x[0] for x in circle2]
    circle2_y = [x[1] for x in circle2]
    # plt.scatter(circle2_x, circle2_y, color='b')
    for i in circle2:
        obstaclespace[i[1]][i[0]] = -1


# Object 4 = rectangle_obstacle_1
    sideE = []
    sideF = []
    sideG = []
    sideH = []
    
    for x in range(1001):
        for y in range(1001):
            if x-(3.75*100-d) >= 0:
                sideE.append((x, y))
            if x-(6.25*100+d) <= 0:
                sideF.append((x, y))
            if y-(4.25*100-d) >= 0:
                sideG.append((x, y))
            if y-(5.75*100+d) <= 0:
                sideH.append((x, y))
           
    rectangle1side = list(set(sideE) & set(sideF) & set(sideG) & set(sideH))
    for i in rectangle1side:
        obstaclespace[i[1]][i[0]] = -1
    x_rectangle1 = [x[0] for x in rectangle1side]
    y_rectangle1 = [x[1] for x in rectangle1side]
    # plt.scatter(x_rectangle1, y_rectangle1, color='b')


# Object 5 = rectangle_obstacle_2
    sideI = []
    sideJ = []
    sideK = []
    sideL = []

    for x in range(1001):
        for y in range(1001):
            if x-(7.25*100-d) >= 0:
                sideI.append((x, y))
            if x-(8.75*100+d) <= 0:
                sideJ.append((x, y))
            if y-(2*100-d) >= 0:
                sideK.append((x, y))
            if y-(4*100+d) <= 0:
                sideL.append((x, y))
           
    rectangle2side = list(set(sideI) & set(sideJ) & set(sideK) & set(sideL))
    for i in rectangle2side:
        obstaclespace[i[1]][i[0]] = -1
    x_rectangle2 = [x[0] for x in rectangle2side]
    y_rectangle2 = [x[1] for x in rectangle2side]
    # plt.scatter(x_rectangle2, y_rectangle2, color='b')

    obstacle_t = obstaclespace.T
    obs = []
    for i in range(1001):
        obs.append(obstacle_t[i])
    
    # plt.show()
    # plt.savefig("Map.png")
    return obs, boundary_x, boundary_y