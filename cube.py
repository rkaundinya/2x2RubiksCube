import random
from queue import Queue
from queue import PriorityQueue
from collections import deque
from node import Node
from solutionData import Solution
from solutionData import idaStarSolution
from solutionData import rbfsSolution
import string
import time
import cubeData
import sys

class cube:

  def __init__(self, string="WWWW RRRR GGGG YYYY OOOO BBBB"):
    # normalize stickers relative to a fixed corner
    currentState = string.replace(" ", "")
    currentState += " "
    self.state = list(currentState)
    return
    
  def norm(self):
    newState = [None] * len(self.state)
    # newState = self.state.copy()

    tenColor = self.state[10]
    twelveColor = self.state[12]
    nineteenColor = self.state[19]

    tenOppositeColor = cubeData.COLOR_OPPOSITES[tenColor]
    twelveOppositeColor = cubeData.COLOR_OPPOSITES[twelveColor]
    nineteenOppositeColor = cubeData.COLOR_OPPOSITES[nineteenColor]

    tenSwitch = ""
    tenOppositeSwitch = ""
    twelveSwitch = ""
    twelveOppositeSwitch = ""
    nineteenSwitch = ""
    nineteenOppositeSwitch = ""

    if tenColor == "G":
      tenSwitch = tenColor
      tenOppositeSwitch = tenOppositeColor
    else:
      tenSwitch = "G"
      tenOppositeSwitch = cubeData.COLOR_OPPOSITES["G"]
    
    if twelveColor == "Y":
      twelveSwitch = twelveColor
      twelveOppositeSwitch = twelveOppositeColor
    else:
      twelveSwitch = "Y"
      twelveOppositeSwitch = cubeData.COLOR_OPPOSITES["Y"]

    if nineteenColor == "O":
      nineteenSwitch = nineteenColor
      nineteenOppositeSwitch = nineteenOppositeColor
    else:
      nineteenSwitch = "O"
      nineteenOppositeSwitch = cubeData.COLOR_OPPOSITES["O"]

    colorSwitchCode = {
      tenColor : tenSwitch,
      tenOppositeColor : tenOppositeSwitch,
      twelveColor : twelveSwitch,
      twelveOppositeColor : twelveOppositeSwitch,
      nineteenColor : nineteenSwitch, 
      nineteenOppositeColor : nineteenOppositeSwitch,
    }

    count = 0

    for color in self.state:
      if color == " ": 
        newState[count] = " "
        continue
      newState[count] = colorSwitchCode[color]
      count += 1

    self.state = newState

  def equals(self, cube):
    if (self.state == cube.state):
      return True 

    return False 

  def clone(self):
    return cube(''.join(self.state))

    # apply a move to a state
  def applyMove(self, move, printEachMove = False):
    assert(cubeData.MOVES[move])
    moveToMake = cubeData.MOVES[move]
      
    initialState = [None] * len(self.state)
    count = 0
    for i in self.state:
      initialState[count] = i
      count += 1

    for i in range(len(moveToMake)):
      self.state[i] = initialState[moveToMake[i]]

    if (printEachMove):
      self.print()
      print()

  def applyMoveToState(self, move):
    assert(cubeData.MOVES[move])
    moveToMake = cubeData.MOVES[move]
      
    initialState = [None] * len(self.state)
    newState = [" "] * len(self.state)
    count = 0
    for i in self.state:
      initialState[count] = i
      count += 1

    for i in range(len(moveToMake)):
      newState[i] = initialState[moveToMake[i]]

    self.state = newState
    return newState

  def applyMovesStr(self, alg, printEachMove = False):
    alg = alg.replace(" ", "")
    algLength = len(alg)
    moveToApply = ""
    myIter = iter(range(len(alg)))
    for i in myIter:
      moveToApply = alg[i]
      if (i < algLength - 1 and alg[i+1] == "'"):
        moveToApply += "'"
        next(myIter)

      self.applyMove(moveToApply, printEachMove)

    # apply a string sequence of moves to a state
  def applyMovesToPrint(self, alg):
    alg = alg.replace(" ", "")
    algLength = len(alg)
    moveToApply = ""
    states = []
    states.append(self.state)
    myIter = iter(range(len(alg)))
    for i in myIter:
      moveToApply = alg[i]
      if (i < algLength - 1 and alg[i+1] == "'"):
        moveToApply += "'"
        next(myIter)

      states.append(self.applyMoveToState(moveToApply))

    self.printInThrees(states)
          

    # check if state is solved
  def isSolved(self):
    solvedState = list("WWWWRRRRGGGGYYYYOOOOBBBB ")
    if (self.state == solvedState):
      return True 

    return False

    # print state of the cube
  def print(self):
    topRow = [0,1]
    secondRow = [2,3]
    thirdRow = [16, 17, 24, 8, 9, 24, 4, 5, 24, 20, 21]
    fourthRow = [18, 19, 24, 10, 11, 24, 6, 7, 24, 22, 23]
    fifthRow = [12, 13]
    sixthRow = [14, 15]

    print("   ", end = "")
    for i in topRow:
      print(self.state[i], end="")
    
    print()
    print("   ", end="")

    for i in secondRow:
      print(self.state[i], end = "")
    
    print()
    
    for i in thirdRow:
      print(self.state[i], end="")
    
    print()

    for i in fourthRow:
      print(self.state[i], end = "")
    
    print()
    print("   ", end = "")

    for i in fifthRow:
      print(self.state[i], end = "")

    print()
    print("   ", end = "")

    for i in sixthRow:
      print(self.state[i], end = "")
      
    print()

  def printInThrees(self, states):
    topRow = [0,1]
    secondRow = [2,3]
    thirdRow = [16, 17, 24, 8, 9, 24, 4, 5, 24, 20, 21]
    fourthRow = [18, 19, 24, 10, 11, 24, 6, 7, 24, 22, 23]
    fifthRow = [12, 13]
    sixthRow = [14, 15]
    
    numStates = len(states)
    threePairs = numStates // 3

    # Keep track of if we have non multiple of 3 cubes to print
    remainingCubes = numStates - (threePairs * 3)

    # If so then make sure to add one to cube print iteration
    overFlowPairs = 0
    if remainingCubes != 0:
      overFlowPairs = 1

    for i in range(threePairs + overFlowPairs):
      pairNum = 3 * i
      cubePrintRange = 3
      if overFlowPairs > 0 and i == threePairs:
        cubePrintRange = remainingCubes

      print("   ", end="")
      for j in range(cubePrintRange):
        for cube in topRow:
          print(states[pairNum + j][cube], end="")
        # gap of 12
        print("            ", end="")
      
      print()
      print("   ", end="")
      for j in range(cubePrintRange):
        for cube in secondRow:
          print(states[pairNum + j][cube], end="")
        # gap of 12
        print("            ", end="")

      
      print()
      for j in range(cubePrintRange):
        for cube in thirdRow:
          print(states[pairNum + j][cube], end="")
        print("   ", end="")

      print()
      for j in range(cubePrintRange):
        for cube in fourthRow:
          print(states[pairNum + j][cube], end="")
        print("   ", end="")

      print()
      print("   ", end="")
      for j in range(cubePrintRange):
        for cube in fifthRow:
          print(states[pairNum + j][cube], end="")
        # gap of 12
        print("            ", end="")

      print()
      print("   ", end="")
      for j in range(cubePrintRange):
        for cube in sixthRow:
          print(states[pairNum + j][cube], end="")
        # gap of 12
        print("            ", end="")

      print("\n\n")

  def printSolution(self, solution):
    movesStr = ""

    if isinstance(solution, Solution):
      movesStr = solution.solution
    elif isinstance(solution, idaStarSolution):
      movesStr = solution.path
    
    print(movesStr)
    self.applyMovesToPrint(movesStr)
    print("Explored Nodes: " + str(solution.iterations))
    print("Time: " + str(solution.time))

  def shuffle(self, n):
    self.state = list("WWWWRRRRGGGGYYYYOOOOBBBB ")
    possibleMoves = ["U", "U'", "R", "R'", "F", "F'", "D", "D'", "L", "L'", "B", "B'"]
    randomMoves = ""
    for i in range(0,n):
      randomMoves += possibleMoves[random.randint(0,11)]

    self.applyMovesStr(randomMoves)
    return randomMoves

  def randomWalk(self, moves, numRandMovesToTry, secsToRun):
    self.state = list("WWWWRRRRGGGGYYYYOOOOBBBB ")
    possibleMoves = ["U", "U'", "R", "R'", "F", "F'", "D", "D'", "L", "L'", "B", "B'"]
    
    # Apply inputted series of moves and store as initial state
    self.applyMovesStr(moves)

    if (self.isSolved()):
      print("No permutations needed - cube is already solved")
      return

    clone = self.clone()

    numIterations = 0
    startTime = time.time()
    secsRan = 0

    # Run this for the time specified by user via command line arg
    while secsRan < secsToRun:
      numIterations += 1
      randomMoves = ""

      # Reset clone state to initial state
      clone = self.clone()

      # Generate a random walk
      for i in range(0,numRandMovesToTry):
        randomMoves += possibleMoves[random.randint(0,11)]
      
      # Apply the random walk
      clone.applyMovesStr(randomMoves)

      if (clone.isSolved()):
        # Get current time for more precise time measure
        secsRan = time.time() - startTime
        # Print the list of moves that got the goal state
        print(randomMoves)
        # Print the initial state
        print("Initial State:")
        self.print()
        # Print the rubiks cube state after each move
        print("Moves visualized:")
        self.applyMovesStr(randomMoves, True)
        print("Number of iterations: " + str(numIterations))
        print("Seconds Ran: " + str(secsRan))
        return
        
      # Update time ran so far if not solved
      secsRan = time.time() - startTime

    print("No solution in the time limit!")

  def breadthFirstSearch(self):
    startTime = time.time()
    open = Queue()
    open.put(Node(self.state))

    numExploredNodes = -1
    closed = {}
    while open:
      # Get the current open node
      currentNode = open.get()
      currentNode.norm()

      # If node is at goal state return moves to goal
      if (currentNode.atGoal()):
        return Solution(currentNode.getMoves(), numExploredNodes, time.time() - startTime)
      
      # Otherwise, add to closed dictionary
      closed[tuple(currentNode.state)] = ""

      # Keep count of number of nodes explored
      numExploredNodes += 1

      # Now iterate through all moves and find child states
      for i in currentNode.getPossibleMoves():
        # Make child node
        clone = currentNode.clone()
        clone.applyMove(i)

        # If child node state not in closed, add to open list
        if tuple(clone.state) not in closed:
          open.put(clone)

    print("Goal not found")
    return Solution()

  def manhattanDistance(self, state):
    totalDist = 0
    face = 0
    count = -1
    for i in state:
      if i == " ":
        break
      count += 1
      face = count // 4
      if face == 0:
        if i == "W":
          continue
        elif i == "Y":
          totalDist += 2
        else:
          totalDist += 1
      elif face == 1:
        if i == "R":
          continue
        elif i == "O":
          totalDist += 2
        else:
          totalDist += 1
      elif face == 2:
        if i == "G":
          continue
        elif i == "B":
          totalDist += 2
        else:
          totalDist += 1
      elif face == 3:
        if i == "Y":
          continue
        elif i == "W":
          totalDist += 2
        else:
          totalDist += 1
      elif face == 4:
        if i == "O":
          continue
        elif i == "R":
          totalDist += 2
        else:
          totalDist += 1
      elif face == 5:
        if i == "B":
          continue
        elif i == "G":
          totalDist += 2
        else:
          totalDist += 1
    totalDist /= 8
    return totalDist

  def aStarSearch(self):
    startTime = time.time()
    fCost =  self.manhattanDistance(self.state)
    open = PriorityQueue()
    initialNode = Node(self.state)
    initialNode.norm()
    open.put((fCost, initialNode))
    frontierCheck = {}
    closed = {}

    numIterations = -1

    while open:
      numIterations += 1
      currentNode = open.get()[1]
      currentNode.norm()
      if tuple(currentNode.state) in frontierCheck.keys():
        del frontierCheck[tuple(currentNode.state)]

      if (currentNode.atGoal()):
        return Solution(currentNode.getMoves(), numIterations, time.time() - startTime)
      closed[tuple(currentNode.state)] = ""

      for i in currentNode.getPossibleMoves():
        clone = currentNode.clone()
        clone.norm()
        clone.applyMove(i)
        clone.setDepth(clone.depth + 1)
        if tuple(clone.state) not in closed.keys() and tuple(clone.state) not in frontierCheck.keys():
          fcost = clone.depth + self.manhattanDistance(clone.state)
          open.put((fcost, clone))
          frontierCheck[tuple(clone.state)] = ""

    return Solution("Failure")

  def idaStar(self):
    currentbound = self.manhattanDistance(self.state)
    path = deque()
    initialNode = Node(self.state)
    initialNode.norm()
    path.append(initialNode)
    openStates = {}
    openStates[tuple(self.state)] = ""
    nodesExplored = 0
    startTime = time.time()
    while True:
      solution = self.idaStarSearch(path, openStates, 0, currentbound, nodesExplored, startTime)
      if solution.solutionFound == "Found":
        return solution
      elif solution.cost < 0.0: # Assuming no negative costs, using negative values to represnt infinity
        solution.time = time.time() - solution.time
        return solution
      currentbound = solution.cost


  def idaStarSearch(self, path, openStates, gCost, currentbound, nodesExplored, timeStamp):
    pathLength = len(path)
    # currentNode = path[pathLength - 1]
    currentNode = path[-1]
    fCost = gCost + self.manhattanDistance(currentNode.state)
    if fCost > currentbound:
      return idaStarSolution("", currentNode.getMoves(), fCost, nodesExplored, time.time() - timeStamp)
    if currentNode.atGoal():
      return idaStarSolution("Found", currentNode.getMoves(), fCost, nodesExplored, time.time() - timeStamp)
    minCost = sys.maxsize
    nodesExplored += 1
    for nextMove in currentNode.getPossibleMoves():
      clone = currentNode.clone()
      # TODO - Overload equals operator in node class
      clone.applyMove(nextMove)
      clone.norm()
      if clone not in openStates:
        path.append(clone)
        solution = self.idaStarSearch(path, openStates, gCost + 1, currentbound, nodesExplored, timeStamp)
        if solution.solutionFound == "Found":
          return solution 
        if solution.cost < minCost:
          minCost = solution.cost
        if tuple(clone.state) in openStates:
          del openStates[tuple(clone.state)]

        path.pop()

    return idaStarSolution("NotFound", currentNode.getMoves(), minCost, nodesExplored, time.time() - timeStamp)

  # The best runtime algorithm I had which also returned an optimal solution was a* without doing norm
  def competitionAlg(self):
    startTime = time.time()
    fCost =  self.manhattanDistance(self.state)
    open = PriorityQueue()
    initialNode = Node(self.state)
    #initialNode.norm()
    open.put((fCost, initialNode))
    frontierCheck = {}
    closed = {}

    numIterations = -1

    while open:
      numIterations += 1
      currentNode = open.get()[1]
      #currentNode.norm()
      if tuple(currentNode.state) in frontierCheck.keys():
        del frontierCheck[tuple(currentNode.state)]

      if (currentNode.atGoal()):
        return Solution(currentNode.getMoves(), numIterations, time.time() - startTime)
      closed[tuple(currentNode.state)] = ""

      for i in currentNode.getPossibleMoves():
        clone = currentNode.clone()
        #clone.norm()
        clone.applyMove(i)
        clone.setDepth(clone.depth + 1)
        if tuple(clone.state) not in closed.keys() and tuple(clone.state) not in frontierCheck.keys():
          fcost = clone.depth + self.manhattanDistance(clone.state)
          open.put((fcost, clone))
          frontierCheck[tuple(clone.state)] = ""

    return Solution("Failure")

  def simplerbfs(self, node, bound):
    if node.fCost > bound:
      return node
    if node.atGoal():
      return node

    successors = PriorityQueue()
    for move in node.getPossibleMoves():
      clone = node.clone()
      clone.applyMove(move)
      clone.setDepth(clone.depth + 1)
      successors.put((clone.depth + self.manhattanDistance(clone.state), clone))
    best = successors.get()[1]
    while best.fCost <= bound:
      secondBestCost = successors.queue[0][0]
      best = self.simplerbfs(best, min(best.fCost, secondBestCost))
      if (best.atGoal()):
        break
      successors.put((best.fCost, best))
    
    return best

  def recursiveBestFirstSearch(self):
    node = Node(self.state)
    #node.norm()
    node.fCost = self.manhattanDistance(node.state)
    solution = self.recursiveBFSInternal(node, float("inf"))
    solution.time = time.time() - solution.time
    return solution

  def recursiveBFSInternal(self, node, fLimit, nodesExplored = 0, timeStamp = time.time()):
    successors = PriorityQueue()
    if node.atGoal():
      return rbfsSolution(node, node.getMoves(), nodesExplored, timeStamp)

    nodesExplored += 1
    for move in node.getPossibleMoves():
      clone = node.clone()
      clone.applyMove(move)
      clone.setDepth(clone.depth + 1)
      #clone.norm()
      clone.fCost = max(clone.depth + self.manhattanDistance(clone.state), node.fCost)
      successors.put((clone.fCost, clone))

    while True:
      best = successors.get()[1]

      # If current best node cost is greater than our stored second best node cost
      # If so, rewind back to last recursion level (predecessor in tree)
      # If not, we have a better solution so keep looking at children
      if best.fCost > fLimit:
        return rbfsSolution(best, "Failure", nodesExplored, timeStamp)
      # Make sure to get the 
      altBestfCost = fLimit
      if not successors.empty():
        altBest = successors.queue[0][1]
        altBestfCost = altBest.fCost

      solution = self.recursiveBFSInternal(best, min(fLimit, altBestfCost), nodesExplored, timeStamp)
      best = solution.node
      successors.put((best.fCost, best))
      # successors.put((altBest.fCost, altBest))
      if solution.solution != "Failure":
        return solution
      

  def iterativeDeepeningSearch(self, maxDepth):
    exploredNodeCount = 1
    for i in range(maxDepth):
      print("Depth: " + str(i), end = " ")
      result = self.depthLimitedSearch(i)
      print("d: " + str(result.iterations - exploredNodeCount))
      exploredNodeCount = result.iterations
      if result.solution != "Cutoff":
        return result

    print("Failed to find solution")
    return Solution("Failure")

  def depthLimitedSearch(self, depthLimit):
    startTime = time.time()
    stack = deque()
    parentsInStack = {}

    result = Solution("Failure")    
    numberOfIterations = -1

    node = Node(self.state)
    node.norm()
    stack.append(node)
    while stack:
      numberOfIterations += 1
      currentNode = stack.pop()

      if tuple(currentNode.state) in parentsInStack.keys():
        del parentsInStack[tuple(currentNode.state)]
      
      if (currentNode.atGoal()):
        return Solution(currentNode.getMoves(), numberOfIterations, time.time() - startTime)
      if currentNode.depth == depthLimit:
        result = Solution("Cutoff", numberOfIterations)
      elif tuple(currentNode.state) not in parentsInStack:
        for i in cubeData.MOVES.keys():
          clone = currentNode.clone()
          clone.setDepth(clone.depth + 1)
          clone.applyMove(i)
          clone.norm()
          stack.append(clone)
          parentsInStack[tuple(clone.state)] = ""
    return result
        
  def recursiveDLS(self, limit):
    counter = Solution("Failure", 0)
    node = Node(self.state)
    node.norm()
    return self.recursiveDLSHelper(node, limit, counter)
    
  def recursiveDLSHelper(self, node, limit, result, startTime = time.time()):
    cutoffOccured = False

    if (node.atGoal()):
      return Solution(node.getMoves(), result.iterations, time.time() - startTime)
    elif (node.depth == limit):
      return Solution("Cutoff", result.iterations, result.time)
    else:
      result.iterations += 1
      for i in node.getPossibleMoves():
        clone = node.clone()
        clone.norm()
        clone.setDepth(clone.depth + 1)
        clone.applyMove(i)
        result = self.recursiveDLSHelper(clone, limit, result, startTime)

        if result.solution == "Cutoff":
          cutoffOccured = True
        elif result.solution != "Failure":
          return result
    if cutoffOccured == True:
      return Solution("Cutoff", result.iterations, time.time() - startTime)
    
    return Solution("Failure", result.iterations, time.time() - startTime)

  def iterativeDeepeningSearchRecursive(self, maxDepth):
    exploredNodeCount = 0
    for i in range(maxDepth):
      print("Depth: " + str(i), end = " ")
      result = self.recursiveDLS(i)
      # Cache this early so that we can print the correct num of nodes if we found a solution
      bFoundSolution = result.solution != "Cutoff"

      # Return nodes we iterated over if we found a solution without subtracting
      # total previously iterated
      if bFoundSolution:
        exploredNodeCount = 0

      print("d: " + str(result.iterations - exploredNodeCount))
      exploredNodeCount = result.iterations
      if result.solution != "Cutoff":
        return result

    print("Failed to find solution")
    return Solution("Failed to find solution")