Can run this script by either running the .sh file or by opening RubiksCube.py in your favorite IDE and running with console commands. 

Commands you can use:
print - prints a default cube
print "WWWR RRRW GGGY YYYG OOOB BBBO" - prints a cube with your custom letter layout
goal "WWWW RRRR GGGG YYYY OOOO BBBB" - prints true if the cube you entered is solved, false if not
applyMovesStr "F U" - applies the moves indicated to a default cube and prints the permutated cube; all possible moves: [ U , U', R , R', F , F', D , D', L , L', B , B'] where ' indicates counter clockwise, U is up, R is rear, F is front, D is down, L is left, B is back faces respectively
shuffle 5 - takes a default cube, shuffles it for the number of times indicated, and prints the cube
bfs "F U" - permutes a default cube with provided moves and performs a breadth first search to find the solution and return sequence of moves
astar "F U" - applies indicated moves to a default cube and performs astar search to return the moves required to fix the permutated cube back to solution
idastar "F U" - applies indicated moves to default cube and solves using iterative deepening astar
competition "F U" - a relic of past engineering; was using a Manhattan Distance heuristic which overestimates cost to goal (not admissible) but overestimates all costs equally such that algorithm can arrive at solution faster
norm "WWWR RRRW GGGY YYYG OOOB BBBO" - takes a provided cube and normalizes it such that it appears in a normalized face order
applyMovesStr "WWWR RRRW GGGY YYYG OOOB BBBO" "F U" - takes a custom cube and applies provided moves to it returning cube after moves were made
dls "F U" 3 - permutes a default cube with provided moves and performs a depth limited search to arrive at a possible solution (may not arrive at a solution depending on provided depth)
ids "F U" 9 - permutes a default cube with provided moves, performs iterative deepening search with max depth provided to arrive at a solution (may not arrive at a solution depending on provided depth)
random "F U" 5 60 - permutes a default cube with given instructions and tries random move combinations with given move length (5 here) for upto given time (60 seconds here)

