from tkinter import *
import random

def polygon_point(polygon, pt):
    """checks if a point is inside of a polygon

    Args:
        polygon (tupple): points of a polygon
        pt (tupple): point to check for

    Returns:
        boolean: True if the point is inside the polygon
    """    
    ans = False
    for i in range(len(polygon)):
        x0, y0 = polygon[i]
        x1, y1 = polygon[(i + 1) % len(polygon)]
        if not min(y0, y1) < pt[1] <= max(y0, y1):
            continue
        if pt[0] < min(x0, x1):
            continue
        cur_x = x0 if x0 == x1 else x0 + (pt[1] - y0) * (x1 - x0) / (y1 - y0)
        ans ^= pt[0] > cur_x
    return ans

def points_inside(points,rc):
    """gets the points inside of a polygon and outputs them in a list

    Args:
        points (tupple): points of a polygon
        rc (tupple): size of canvas to check within

    Returns:
        list: list of the points inside of the polygon
    """
    rc += 1
    p = []
    for x in range(rc):
        for y in range(rc):
            pt = (x,y)
            #print(pt)
            yon = polygon_point(points, pt)
            
            if yon == True:
                #print(pt)
                p.append(pt)
            y = y+1
        x = x+1
    return p

def line_allowed_x(start_point,x_length,points_covered):
    """first checks if the line would be inside the canvas then if it goes into a point that is already a rectangle

    Args:
        start_point (tupple): starting point of the line
        x_length (int): the length of the x line to be added onto the starting point
        points_covered (list): current list of points that are already covered

    Returns:
        boolean: true if the line is allowed
    """    
    if (start_point[0] + x_length) > 100:
        return False
    ran = range(start_point[0], start_point[0] + x_length+1)
    print("ran ",ran)
    for d in ran:
        if (d, start_point[1]) in points_covered:
            print((d, start_point[1]),"is in")
            return False
    return True

def line_allowed_y(start_point,y_length,points_covered):
    """first checks if the line would be inside the canvas then if it goes into a point that is already a rectangle

    Args:
        start_point (tupple): starting point of the line
        y_length (int): the length of the y line to be added onto the starting point
        points_covered (list): current list of points that are already covered

    Returns:
        boolean: true if the line is allowed
    """    
    if (start_point[1] + y_length) > 100:
        return False
    ran = range(start_point[1], start_point[1] + y_length+1)
    print("range ",ran)
    for d in ran:
        if (d, start_point[0]) in points_covered:
            print((d, start_point[0]),"is in")
            return False
    return True
def line_allowed(start, end,points_covered):
    
    if (max(end)) > 100:
        return False
    ran = range(start[0],end[0])
    for d in ran:
        if (d,start[0]) in points_covered:
            return False
    ran2 = range(start[1],end[1])
    for d in ran2:
        if (start[1],d) in points_covered:
            return False
    return True
def make_recangle_list(r,h):

    main_rect = ((0,0),(r,0),(r,r),(0,r))
    main_points = points_inside(main_rect,r)
    points_covered =[]
    rects = []
    q = 0

    while q < h-1:
        start_point = random.choice(main_points)
        if not start_point in points_covered:
            x_length = random.randint(5,15)
            
            if line_allowed_x(start_point,x_length,points_covered) == True:
                y_length = random.randint(5,15)
                
                if line_allowed_y(start_point,y_length,points_covered) == True:
                    print("Rectangle Made")
                    rect_outline = (start_point,(start_point[0],start_point[1] + y_length),(start_point[0] + x_length,start_point[1] + y_length),(start_point[0]+x_length,start_point[1]))
                    rects.append(rect_outline)
                    points_covered.extend(points_inside(rect_outline,100))
                    main_points = list(set(main_points) - set(points_covered))
                    q += 1
                    print(points_covered)
                else:
                    q -= 1
                    print("line y not allowed")
                    
            else:
                q -= 1
                print("line x not allowed")
        else:
            q -= 1
            print("start point not allowed")
    return rects

# r = int(input("Size of Main?"))
# h = int(input("How Many?"))
canvas_dim = 100
how_many = 10

rects = make_recangle_list(canvas_dim, how_many)

##list of rects to make
master = Tk()
w = Canvas(master, width=canvas_dim, height=canvas_dim)
for rectangle in rects:
    w.create_rectangle(rectangle[0][0], rectangle[0][1], rectangle[3][0], rectangle[1][1], fill="white", outline = 'blue')
w.pack()
master.mainloop()


# need to check if rectangles 2 other lines would go into it