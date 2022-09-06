# a1-forrelease

# Report: B551 Assignment 1: Searching 

# Part 1: The 2021 Puzzle 
### Objective: 

We are given a 2D matrix with 5 rows and 5 columns. It contains tiles numbered from 1 - 25 which is the current state. We need to build an algorithm which can find the shortest sequence of moves that restores the canonical configuration of the tile board, which is the number increasing order of tiles ranging starting with 1 and ending with 25.[Text Wrapping Break]It is also given that we can move only in 8 principle component directions for our tile board(U, D, L, R , Ic, Icc,  Oc, Occ). 

How did we approached the problem to arrive at the solution:  

- Initially we took the time to understand a problem statement and thought about what will be our successor function. Then we thought that our successor function will have 8 principle moves which are shown below. 

- To solve this problem we needed 2 main functions: Successor and Solve. 

- In successor function we are exploring all the possible combinations from the current state and we are updating our fringe with all this possible states.  

- Successor function also has a part where we hardcoded our logic for our last 4 principle component directions which are U, D, L, R , Ic, Icc,  Oc, Occ. 

For sliding rows, R (right) or L(left), followed by the row number indicating the row to move left or  right.  The row numbers range from 1-5. 

For sliding columns, U (up) or D (down), followed by the column number indicating the column to move up or down.  The column numbers range from 1-5. 

For rotations, I (inner) or O (outer), followed by whether the rotation is clockwise  (c)  or counterclockwise (cc) 

- Next comes our Solve function where we are using  A* search Algorithm. In this we are taking states which have minimum value associated with them. This minimum value is coming from 2 important components: Heuristic function and cost function. 

- Initially we thought of using Number of misplaced tiles on a given tile board as Heuristic. Everytime we encounter a new board we calculate the number of misplaced tiles and add that number to our cost function but this is not an admissible heuristic function because every time we get a new Heuristic value it is overestimating misplaced tiles after every iteration. Consider a situation where we can get our answer by doing L1 move which will cost only 1 unit but our misplaced tile function says it will take 4 units because it has 4 misplaced tiles. So, this way it was overestimating.  

- We are using Manhattan distance as our heuristic function. We were calculating Manhattan distance for every tile in the newly created board, passing this  distance value as Heuristic function value, but this is not an admissible heuristic because every time we get a new Heuristic value it is overestimating distance. So, we made changes to our Manhattan heuristic function. 

- In our problem statement the maximum cost for a Manhattan distance for a tile who is misplaced is 16 units and if we divide our heuristic cost by this 16 then we can get an admissible heuristic who is never going to overestimate. That's why we tried this logic but because our heuristic value becomes very small it will take a lot of time for our goal. This heuristic becomes a weak admissible heuristic and it is underestimating significantly.  

- Cost function for our problem statement is always 1 unit because when we take a step in any direction it’s only 1.  

- Here we are using Searching algorithm Number #2. This way we are systematically exploring optimal moves to reach our goal. How we implemented this algorithm is explained below. 

- In our code we are initially calculating :Total Cost ( f_s )= Heuristic value ( h_s ) + cost value ( c_s )  of current board and appending this  f_s  along with the current board into our fringe. 

- Then we are popping that board from the fringe which has a minimum total cost. If that popped board is our goal then stop at that point and return all the moves we did until now. If that board is not our goal then calculate all the successors of the current board along with their total cost. Then we are pushing all the successors into the fringe and repeating previous steps systematically until we find optimal moves to reach our goal. 

### Details about the Search Abstraction: 

- Search Abstraction Used: As given in question requirement we have used A* algorithm here. A* have 2 important components: Heuristic Function and Cost Function. This algorithm will surely find the optimal goal state when used with admissible heuristic. 

- Set of valid states: A matrix with 5 rows and 5 columns and has tiles numbers ranging from 1 to 25. 

- Initial state: Any state from Set of valid states where we have unique values ranging from  1 to 25 . 

- The successor function: This gives all valid states from the current state. This function gives all states after one iteration of every 8 principle component directions(U, D, L, R , Ic, Icc,  Oc, Occ).  

- Cost function: This problem has a uniform cost which is 1 steps/cost per move in any valid direction (U, D, L, R , Ic, Icc,  Oc, Occ) 

- Heuristic Function: As explained above, we still end up using Manhattan distance. It's not admissible; but it will give an output quite fast - probably a sub-optimal one. 

Goal definition: Goal here is achieved when we reach our canonical position which is the number increasing order of range between 1 and 25 inclusive with minimum iterations (minimum moves of principle components). 

### Questions: 

- In this problem, what is the branching factor of the search tree? 

Our program has 8 principle moves and each of them has their own individual moves such as L ( left ) can be applied on 5 rows which results in 5 unique moves the same goes for R ( right ). Now U ( up ) can be applied on 5 columns which also results in 5 unique moves the same goes for D ( down ). This becomes a total of 20 branches. 

 Now we have I ( inner ) can be applied on the inner circle clockwise and anticlockwise and the same goes for the O ( outer ) circle. Which results total 4 branches.  

If you add all these branching factors then you get a final branching factor of 24. So, finally we can say that our branching factor for this problem is **24**.



- If  the  solution  can  be  reached  in  7  moves,  about  how  many  states  would  we  need  to  explore  before  we found it if we used BFS instead of A* search?

If the solution can be reached in 7 moves, about how many states would we need to explore before we found it if we used BFS instead of A* search? A rough answer is fine. 

In BFS, we explore all the level 1 nodes(24 in this case) and then go into the next level which individually will have 24 branches. So if this can be achieved in 7 steps in A* search, it should be in 7th level. Therefore the maximum it would take for BFS is 24^7 states and minimum is (24^6)+1. 

So the range of states for BFS is in the range [(24^6)+1 : 24^7] 


# Part 2 - Road trip!

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


# Part 3: Choosing Teams 

### Objective: 

- We are given response from the survey which has the preference of each student about their expectation of teams to work in a team assignment. Students can work alone, team of 2 or team of 3. We are expected to form teams that satisfy the team expectations of all people (If possible). We are also given costs to be incurred to evaluate these teams in terms handling these cases/complaints which arises due to Group size conflict, Not getting the member he wants, getting a teammate he didn’t wish to work and also given the time needed to grade these teams. In this part of the assignment, we are expected to get the combinations of teams which have least cost. 

### Problem solving (How we arrived at the solution) 

- We had multiple brainstorming sessions to understand the problem and to discuss how to approach the problem. We soon realized that this is a different kind of problem than first and second since there is no Goal state here and we are expected to get the best possible solution till the program is allowed to run 

- We started thinking in the lines of solving it with BFS or DFS. But the inability to find an exact logical method to determine next steps (logical successor) which would cover all possible combinations, prevented us from deploying BFS or DFS 

- We also couldn’t get the right heuristic here to implement A* since we do not know the Goal state 

- This led us to think about the local search techniques where the goal is to arrive at a reasonable solution rather than the best solution possible. We explored hill descent/gradient descent algorithms to understand how exactly local search techniques work 

- This is where we realized that these techniques could give us suboptimal solution (local minima) when we systematically evaluate the neighbouring states since greedy algorithms always tend to select the best move/node from the current positions/state. Hence, we decided that instead of going with a systematic approach, we wanted to randomize the state selection 

- In this approach, we begin with a random state, evaluate its cost then move to another random next state and evaluate its cost and so on. Here, we always compare these costs and store the state which gives us least cost at a given time 

- We figured out that there are two major issues with this approach-  

(i) The search space can be so huge if the class has high number of students and searching randomly can take very long time 
(ii) With Random state selection, we can’t guarantee that all states would be explored 

- The following section talks about how we tackled the above-mentioned issues 
 
### How we solved these Issues: 

- Search space can be huge when number of students are too many. So we thought of limiting the search space where random function generates next state. First, we evaluated few standard states, which will reduce the random search space. If there are N students, max teams can be N. And since max of 3 people can come in one team, search space is Nx3. But out of all the search spaces there is only one case where N teams can happen (when everyone is in individual team). If we evaluate this state in advance, search space can be reduced to (N-1) x 3. We call it standard states which are evaluated before generating random states. 

- Once we have (N-1) x 3 search space, we can further reduce it by finding out all the combinations of 1 person teaming up with another guy and rest all are in single team. When we find all combinations of this sort, this reduces search space to (N-2) x 3 

- We can’t ensure exploring all states with random state generation unless we maintain a global variable which keeps track of all visited states. But since number of states can be huge with high number of participants, this creates memory issue and program slows down later on. So, we came up with an innovative way to ensure near certainty that explore almost all states. The idea is to start with least number of teams possible. If there are N participants, ceil(N/3) will be the minimum number of states possible. Since we can figure out combinations nC3, we have an idea of how many states are possible with the minimum teams(rows).  

- We start with this layout of ceil(N/3) X 3 board and place each participant in a random place and evaluate the cost of this state. Since we are generating random states, same state can come multiple times. So, we reasoned that number of iterations in this layout has to be higher than nC3 and after a lot of testing, we decided to set the limit to (nC3 * 2), as almost all the times all states were getting covered in this limit. Once this threshold is reached, we introduce another row to this layout which will result into search space of: (ceil(N/3)+1) X 3.  This has to iterate way more times than nC3, so we multiplied the threshold by factor of 2, resulting into (nC3*2*2) iterations. Once these iterations are reached, we introduce another Row (team number). This ensures that in a way we systematically explore random states. 

- Another aspect that we realized is the cost is highest when people team up with someone who they don’t want to work with (10 mins). In order to eliminate placing such people together, we introduced a condition saying no two people who wishes not to work with a person should be put in the same team. We ensured that a state is an acceptable state only if the above condition is met (There is an exception to this, where there is no state can be formed without placing two people who hate each other in the same team. We accept such states after trying to find an alternative placements) 

### Solution Implementation – What does each section in code do 

We define the following functions in the code which focusses on specific aspect of the solution: 
(i) Cost Function 
(ii) Successor Function 
(iii) Solver 
 

- (i) Cost Function 

-It evaluates the total cost of a given state with comparison to the Goal State based on 4 parameters listed in the problem statement: Team grading time, Group size conflict resolution, Time to resolve not getting requested member issue, Time to resolve 'not wish to work' with a member conflict. It takes in two arguments, Goal state and current state 

- (ii) Successor Function 

-This gives out a random state to explore based on the constraints and the proceeding logic which was explained in the previous section.  

 

- (iii) Solver 

-This is the main function which makes use of the above two functions and gives out a dictionary with the best solution attained till now along with its cost. This is where we decide how many rows to start exploring and how to increase the search space in gradual and systematic way 
 

### Details about the Search Abstraction: 

- Set of valid states: All the combinations in which N participants could be arranged in Team of 1, Team of 2 or Team of 3 

- Initial state: We take a random valid state as the initial state with layout of ceil(N/3) X 3 

- The successor function: Since there isn’t a definite way to move around to attain the next state, successor state is a random valid state  

- Cost function: We have the cost function explicitly given in the problem. We have used it 

- Goal state definition: Since there is no definite goal state we know beforehand, we estimate and yield a reasonable state which is with the lowest cost till the time of exploration.


# Credits
- Karan Milind Acharya (karachar)
- Gaurav Narasimha Atavale (gatavale)
- Gaurav Vanmane (gvanmane)



