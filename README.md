# Road trip!

## Formulating the search problem
- Finding a route between two cities on a given map can be extremely compute-intensive if we use un-informed searches like BFS and DFS. Why? Because, *they are unable to decide a **'better'** successor among many options.* They treat all successors the same and just end up computing a lot of unnecessary stuff - leading to extra computation - both in time and memory.
- Informed searches, on the other hand are better suited for problems like this. Rather than selecting 'any' successor among many, they make an informed decision about which one to choose next. How? With the help of a heuristic function.
- A heuristic is extremely helpful in making that decision to choose the next successor to expand. But, a heuristic does not provide us with the actual cost to reach a goal state from an initial state. It just provides us with an estimate.
- Here, we're using A* search - which is a complete & optimal informed search algorithm. Heuristic searches like this are especially important, when the path to reach the goal state is as important as reaching the goal state.

## A brief workflow of the program
1. Maintain a fringe data structure to maintain the paths and nodes.
2. Store the initial node. Calculate it's f(s) = g(s) + h(s); where g(s) = 0, initially.
3. While fringe is non-empty:
    1. Pop the node with the minimum f(s) value.
    2. If it's the goal, exit and return the route, total distance, total hours and total delivery hours.
    2. Else, visit it. Find all it's successors.
    3. For every successor,
        1. Check if it's already visited. If yes, move to the next one.
        2. Calculate the f(s) value for this one.
        3. Check if this successor is in the fringe. If yes, check it's f(s) value. Compare both the values. Retain the information with the least f(s) value.
        4. If not, simply add to the fringe.

- Depending on the filter function, the way to calculate f(s) changes. Explained below in detail.

## Search Abstraction
- **State Space**: A set of all road segments in the given dataset.
- **Initial State**: The initial city (FROM) which we want to find the route to some destination.
- **Successor**: A set of all nodes(cities and/or junctions in the dataset) connected to the FROM city.
- **Edge Weights**: Depending on our function by which our optimsing our algorithm,
    1. segments - 1 (Uniform for every segment)
    2. distance - The length of the highway segment
    3. time - The time it takes to drive that highway segment assuming it is driven at the specified speed limit for that highway. (time = distance / max. speed limit)
    4. delivery - The time it takes to drive that highway segment with the expectation of a delivery driver making a mistake.
- **Goal State**: The destination city (TO) which we want to find the route from the FROM city.
- **Heuristic function**: The shortest distance between any 2 points on Earth is the haversine distance(HD). This can be computed from the co-ordinates given for (almost) all cities. **We make use of 4 different heuristic functions for 4 different optimising functions - each of them based upon this haversine distance.** Following are those:
    1. segments - (HD(current node, goal node))  / Maximum highway length in the dataset.
    2. distance - (HD(current node, goal node))
    3. time - (HD(current node, goal node)) / Max. Speed limit
    4. delivery - Same as above: (HD(current node, goal node)) / Max. Speed limit

- **Why are these admissible?**
    1. Admissibility criteria: h(s) <= h*(s) where h*(s) is the actual cost between 2 cities.
    2. Haversine distance (HD) is the shortest distance between any 2 points on Earth - It will be always less than the total lengths of the road segments between the current node and the goal node. No road segment was built along the geodesic between 2 cities - It is impossible to do that.
    3. For **distance** filter, the reason stated above directly applies. For others, we explain as below.
    4. In order to find an estimate(heuristic) for the **time** filter, we divide the HD by the maximum value of all the speed limits present in the dataset. This is because, the actual speed limits on each of the highway segments between the current node and the goal node will always be less than or equal to the max. speed limit. When you divide the HD by the max value, you ensure that you never overestimate the actual hours needed to reach the goal node.
    5. Similarly, for the **delivery** filter: Delivery time should always be greater than or equal to normal time. As explained above, the h(s) is admissible for estimating normal time - in other words, will be less than the actual time. By statements 1 & 2, it should also be less than the delivery time. Hence, the same h(s) is admissible here as well.
    6. The actual number of segments to reach the goal from another node <= (HD / max. highway length). This is because, the actual highway length is always less than the max. value. So the h(s) for the **segments** filter will never overestimate.


## Other observations
- Initially, we did not keep track of visited nodes. This caused the program to go back to it's parent nodes again and again and was increasing the program running time.
- Also, in the fringe redundant versions of the same node were being appended each time it was a successor. Now, we only retain the one with the least value.
- This makes our program use Search Algorithm #3. For this our heuristic also needs to be consistent. The hueristics mentioned above are consistent. We extensively tested for multiple examples. The cost of reaching from a parent node to a child node is greater than the difference between the hueristic cost of the parent and child node.
- For nodes which didn't have a corresponding coordinate value in the city-gps.txt file, for that node we're using a h(s) = 0. Initially, we tried to select the minimum/average heuristic value of it's neighbors, but there is a chance it can overestimate. This is because, 1 neighbor may actually be quite far away or towards the opposite side even if it's nearer. A value of 0 will never overestimate - Still shouldn't violate the admissiblity and consistency criteria. (Although haven't tested much on this.)
- Our program is hence, quite fast irrespective of how far our initial and destination cities are. We tested for multiple cities. It quickly finds the distance, hours, delivery hours and number of segments. We compared them with Google Maps to see that they're actually in a very good comparison range.
