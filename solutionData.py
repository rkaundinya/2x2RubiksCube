class Solution:
  def __init__(self, solution="", iterations=-1, time=0.0):
    self.solution = solution
    self.iterations = iterations
    self.time = time

class idaStarSolution:
  def __init__(self, solutionFound="", path="", cost=-1, iterations =-1, time=0.0):
    self.solutionFound = solutionFound
    self.path = path
    self.cost = cost
    self.iterations = iterations
    self.time = time 

class rbfsSolution:
  def __init__(self, node, solution="", iterations=-1, time=0.0):
    self.node = node
    self.solution = solution
    self.iterations = iterations
    self.time = time