#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Karan Milind Acharya[karachar], Gaurav Atavale[gatavale], Gaurav Vanmane[gvanmane]
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import math
import sys

def read_datasets():
    """Method to read & parse both the datasets
    """
    coordinates, connected_cities = dict(), dict()
    speed_limits, highway_lengths = list(), list()

    # Reading city_gps.txt
    f1 = open("city-gps.txt", "r")
    for line in f1.readlines():
        x = line.split(" ")
        coordinates[x[0]] = [float(x[1]), float(x[2])]

    f2 = open("road-segments.txt", "r")
    for line in f2.readlines():
        x = line.strip().split(" ")
        city1, city2 = x[0], x[1]
        if city1 not in connected_cities.keys():
            connected_cities[city1] = []
        connected_cities[city1].append([x[1], x[2], x[3], x[4]])

        if city2 not in connected_cities.keys():
            connected_cities[city2] = []
        connected_cities[city2].append([x[0], x[2], x[3], x[4]])

        highway_lengths.append(int(x[2]))
        speed_limits.append(int(x[3]))

    return coordinates, connected_cities, max(speed_limits), max(highway_lengths)

def get_haversine_distance(node_coord, goal_coord):
    """Calculate Haversine distance between the current node and the goal node 

    Args:
        current_node ([type]): [description]
        goal_node ([type]): [description]
    """
    # Formula to calculate haversine distance adapted from
    # http://www.movable-type.co.uk/scripts/latlong.html

    earth_R = 3950  # Radius of Earth (miles)

    lats = [node_coord[0], goal_coord[0]]
    longs = [node_coord[1], goal_coord[1]]

    # Convert to radians
    # https://www.w3schools.com/python/ref_math_radians.asp
    lats = list(map(math.radians, lats))
    longs = list(map(math.radians, longs))

    delta_lat = lats[1] - lats[0]
    delta_long = longs[1] - longs[0]

    a = math.sin(delta_lat / 2) ** 2 + (math.cos(lats[0]) * math.cos(lats[1]) * math.sin(delta_long / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = earth_R * c

    return d

def get_heuristic_cost(current, goal, filter, max_limit, max_highway_length):

    if filter == 'segments':
        return get_haversine_distance(current, goal) / max_highway_length
    elif filter == 'distance':
        return get_haversine_distance(current, goal)
    elif filter == 'time' or filter == 'delivery':
        return get_haversine_distance(current, goal) / max_limit

def get_connected_nodes(node, segments):
    """Successor function
    Return a list of tuple with each tuple containing the following info:
    1. Next_node name
    2. Distance
    3. Normal Time
    4. Delivery time
    5. Highway name

    Args:
        node ([type]): [description]
    """
    curr_node_name, route_taken, total_miles, total_hours, total_delivery_hours, f_s = node

    connected_nodes = list()
    for segment in segments:
        city_name, highway_length, speed_limit, highway_name = segment
        highway_length, speed_limit = int(highway_length), int(speed_limit)

        # Min. time - as we're assuming car driving at the speed limit
        car_time = float(highway_length / speed_limit)

        delivery_time = car_time
        # If driving at greater than or equal to 50mph, delivery driver will make a mistake
        # Will have to return back to origin city and re-drive till the start of the road
        if speed_limit >= 50:
            trip_time = total_delivery_hours  # Until now
            mistake_probability = math.tanh(highway_length / 1000)
            additional_time = mistake_probability * 2 * (car_time + trip_time)
            delivery_time += additional_time
    
        connected_nodes.append([
            city_name, highway_length, car_time, delivery_time, highway_name
        ])

    return connected_nodes

def get_route(start, end, cost):

    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    fringe = []
    # Read and parse the datasets
    coordinates, connected_segments, max_speed_limit, max_highway_length = read_datasets()

    # print(f"Max SL: {max_speed_limit} ---- Max Highway Length: {max_highway_length}")
    if start != end:  # Check whether we're already not at the goal
        visited = list()
        g_s = 0.0
        goal_coordinates = coordinates[end]
        # h_s = get_haversine_distance(coordinates[start], goal_coordinates)
        h_s = get_heuristic_cost(
            coordinates[start], 
            goal_coordinates, 
            cost, 
            max_speed_limit, 
            max_highway_length
        )
        f_s = g_s + h_s

        fringe.append([start, [], 0, 0.00, 0.00, f_s])

        while fringe:
            # for e in fringe:
            #     print(e)
            # print("\n\n")

            # From the fringe, remove the element with the least f_s
            min_cost_node = fringe.pop(fringe.index(min(fringe, key=lambda x: x[-1])))

            # print("\n\n --------- \nVisiting: \n", min_cost_node)
            curr_node_name, route_taken, total_miles, total_hours, total_delivery_hours, f_s = min_cost_node

            if cost == 'segments':
                g_s = len(route_taken)
            elif cost == 'distance':
                g_s = total_miles
            elif cost == 'time':
                g_s = total_hours
            elif cost == 'delivery':
                g_s = total_delivery_hours

            # Visit city
            if curr_node_name not in visited:
                visited.append(curr_node_name)

            # If we've reached the goal
            if curr_node_name == end:
                return {
                    "total-segments" : len(route_taken), 
                    "total-miles" : total_miles, 
                    "total-hours" : total_hours, 
                    "total-delivery-hours" : total_delivery_hours, 
                    "route-taken" : route_taken
                }

            # Query the connected segments to the current node from the dict
            segments = connected_segments[curr_node_name]

            for next_node in get_connected_nodes(min_cost_node, segments):
                next_node_name, miles, car_hrs, del_hrs, highway_name = next_node

                # No need to consider already visited nodes
                if next_node_name in visited:
                    # print(f"\n Already visited --{next_node}---- . Skipping...")
                    continue

                next_route = [(next_node_name, f"{highway_name} for {miles} miles")]

                if cost == 'segments':
                    f_s = float(g_s + 1)
                elif cost == 'distance':
                    f_s = float(g_s + miles)
                elif cost == 'time':
                    f_s = float(g_s + car_hrs) 
                elif cost == 'delivery':
                    f_s = float(g_s + del_hrs)

                # We can only calculate the h_s if we have the coordinates of the next_node
                # Else h_s = 0 will never overestimate
                if next_node_name in coordinates.keys():
                    f_s += get_heuristic_cost(
                        coordinates[next_node_name], 
                        goal_coordinates, 
                        cost, 
                        max_speed_limit,
                        max_highway_length
                    )
            
                element = [
                    next_node_name,
                    route_taken + next_route, 
                    float(total_miles + miles),
                    total_hours + car_hrs,
                    total_delivery_hours + del_hrs,
                    f_s
                ]

                # print(f"\nChecking whether {next_node_name} is in the fringe...")
                i, next_node_in_fringe = None, False
                for index, f in enumerate(fringe):
                    if element[0] == f[0]:
                        i = index
                        next_node_in_fringe = True
                
                if next_node_in_fringe:
                    if fringe[i][-1] > f_s:
                        fringe.pop(i)
                        next_node_in_fringe = False
                
                if not next_node_in_fringe:
                    fringe.append(element)
        
    return {
        "total-segments" : 0, 
        "total-miles" : 0, 
        "total-hours" : 0.00, 
        "total-delivery-hours" : 0.00, 
        "route-taken" : {}
    }

        # route_taken = [
        #     ("Martinsville,_Indiana","IN_37 for 19 miles"),
        #     ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
        #     ("Indianapolis,_Indiana","IN_37 for 7 miles")
        # ]
        # total_miles = 51
        # total_hours = 1.07949
        # total_delivery_hours = 1.1364
    
    
    # return {"total-segments" : len(route_taken), 
    #         "total-miles" : total_miles, 
    #         "total-hours" : total_hours, 
    #         "total-delivery-hours" : total_delivery_hours, 
    #         "route-taken" : route_taken}


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


