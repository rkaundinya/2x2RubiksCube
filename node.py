import cubeData

def applyMoveToState(state, move):
    assert(cubeData.MOVES[move])
    moveToMake = cubeData.MOVES[move]

    initialState = state.copy()
    for i in range(len(moveToMake)):
      state[i] = initialState[moveToMake[i]]

class Node:
  def __init__(self, state, moves = None, depth = 0, fCost = 0):
    if isinstance(state, list) and isinstance(moves, str):
      self.state = state.copy()
      self.moves = moves
      self.depth = depth
      self.fCost = fCost
    elif moves is not None:
      self.state = state.copy()
      self.moves = moves
      self.depth = depth
      self.fCost = fCost
    else:
      self.moves = ""
      self.state = state.copy()
      self.depth = depth
      self.fCost = fCost
  
  def clone(self):
    return Node(self.state, moves=self.moves, depth=self.depth, fCost=self.fCost)

  def setDepth(self, newDepth):
    self.depth = newDepth
  
  def applyMove(self, move):
    self.moves += move
    applyMoveToState(self.state, move)

  def getPossibleMoves(self):
    # Get last move of current node
    lastMove = ""
    lastMoveInverse = ""
    movesLength = len(self.moves)
    if (movesLength > 0):
      lastChar = self.getMoves()[movesLength - 1]
      if lastChar == "'" and movesLength >= 2:
        lastMove += self.getMoves()[movesLength - 2] + lastChar
      else:
        lastMove = self.getMoves()[movesLength - 1]
      lastMoveInverse = cubeData.MOVE_INVERSES[lastMove]

    complementLetter = ""
    threeConsecutiveMoves = False
  
    if movesLength >= 3:
      lastMovesLength = len(lastMove)
      secondToLastMove = ""
      if self.moves[movesLength - lastMovesLength - 1] == "'":
        secondToLastMove = self.moves[movesLength - lastMovesLength - 2] + self.moves[movesLength - lastMovesLength - 1]
      else:
        secondToLastMove = self.moves[movesLength - lastMovesLength - 1]

      secondToLastMoveLength = len(secondToLastMove)

      # Only look for a third move if we haven't finisehd looking at all moves in string
      lastMovesLength += secondToLastMoveLength
      if lastMovesLength != movesLength:
        if self.moves[movesLength - lastMovesLength - 1] == "'":
          complementLetter = self.moves[movesLength - lastMovesLength - 2] + self.moves[movesLength - lastMovesLength - 1]
        else:
          complementLetter = self.moves[movesLength - lastMovesLength - 1]

      # If all 3 previous moves were the same
      if complementLetter != "" and secondToLastMove == lastMove and complementLetter == lastMove:
        threeConsecutiveMoves = True
      """ if (lastMove == self.moves[movesLength - 2]):
        complementLetter = self.moves[lastMove - 3]
      if lastMove == self.moves[movesLength - 2] and lastMove == self.moves[movesLength - 3]:
        threeConsecutiveMoves = True"""
    
    possibleMoves = []
    for move in cubeData.MOVES.keys():
      # Filter out inverse moves (moves that get us to the same state as before the last move)
      if (move == lastMoveInverse):
        continue 
      
      if complementLetter and complementLetter == move:
        continue

      if threeConsecutiveMoves and move == lastMove:
        continue

      possibleMoves.append(move)

    return possibleMoves

  def __lt__(self, other):
    if self.state == other.state:
      return True
    return False

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
      
    # print()

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

  def normNoModify(self):
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
    
    return newState

  def atGoal(self):
    solvedState = list("WWWWRRRRGGGGYYYYOOOOBBBB ")
    if (self.state == solvedState):
      return True 

    return False

  def getMoves(self):
    return self.moves
