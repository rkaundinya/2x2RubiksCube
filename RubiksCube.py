import sys
from cube import cube
from node import Node

# different moves
# https://ruwix.com/online-puzzle-simulators/2x2x2-pocket-cube-simulator.php

'''
sticker indices:

      0  1
      2  3
16 17  8  9   4  5  20 21
18 19  10 11  6  7  22 23
      12 13
      14 15

face colors:

    0
  4 2 1 5
    3

moves:
[ U , U', R , R', F , F', D , D', L , L', B , B']
'''  

# Main Code:
commandLineArgsLength = len(sys.argv)

if commandLineArgsLength == 2:
  if (sys.argv[1] == "print"):
    defaultCube = cube()
    defaultCube.print()
elif commandLineArgsLength == 3:
  # TODO - add argv2 error checking
  if (sys.argv[1] == "print"):
    customCube = cube(sys.argv[2])
    customCube.print()
  elif (sys.argv[1] == "goal"):
    customCube = cube(sys.argv[2])
    if (customCube.isSolved()):
      print("True")
    else:
      print("False")
  elif (sys.argv[1] == "applyMovesStr"):
    defaultCube = cube()
    defaultCube.applyMovesStr(sys.argv[2])
    defaultCube.print()
  elif (sys.argv[1] == "shuffle"):
    defaultCube = cube()
    shuffleMoves = defaultCube.shuffle(int(sys.argv[2]))
    print(shuffleMoves)
    defaultCube.print()
  elif (sys.argv[1] == "bfs"):
    defaultCube = cube()
    defaultCube.applyMovesStr(sys.argv[2])
    solution = defaultCube.breadthFirstSearch()
    defaultCube.printSolution(solution)
  elif (sys.argv[1] == "astar"):
    defaultCube = cube()
    defaultCube.applyMovesStr(sys.argv[2])
    solution = defaultCube.aStarSearch()
    defaultCube.printSolution(solution)
  elif (sys.argv[1] == "idastar"):
    defaultCube = cube()
    defaultCube.applyMovesStr(sys.argv[2])
    solution = defaultCube.idaStar()
    defaultCube.printSolution(solution)
  elif (sys.argv[1] == "competition"):
    defaultCube = cube()
    defaultCube.applyMovesStr(sys.argv[2])
    solution = defaultCube.competitionAlg()
    defaultCube.printSolution(solution)
  elif (sys.argv[1] == "norm"):
    customCube = cube(sys.argv[2])
    customCube.norm()
    customCube.print()
      
elif commandLineArgsLength == 4:
  if (sys.argv[1] == "applyMovesStr"):
    customCube = cube(sys.argv[3]) 
    customCube.applyMovesStr(sys.argv[2])
    customCube.print()
  if (sys.argv[1] == "dls"):
    defaultCube = cube()
    defaultCube.applyMovesStr(sys.argv[2])
    solution = defaultCube.recursiveDLS(int(sys.argv[3]))
    defaultCube.printSolution(solution)
  if (sys.argv[1] == "ids"):
    defaultCube = cube()
    defaultCube.applyMovesStr(sys.argv[2])
    # perform iterative deepening search
    solution = defaultCube.iterativeDeepeningSearchRecursive(int(sys.argv[3]))
    # print results
    defaultCube.printSolution(solution)

elif commandLineArgsLength == 5:
  # Make sure the first argument is the random command
  if (sys.argv[1] == "random"):
    defaultCube = cube()
    # defaultCube.applyMovesStr(sys.argv[2])
    defaultCube.randomWalk(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))