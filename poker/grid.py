from manim import *

SIDE_LENGTH = 0.25

class Grid:
  def __init__(self, rows, cols):
    self._rows = rows
    self._cols = cols
    self._grid = [[None]*cols for _ in range(rows)]

  def __getitem__(self, index):
    return self._grid[index[0]][index[1]]
  
  def __setitem__(self, index, value):
    self._grid[index[0]][index[1]] = value

  def entries(self):
    for row in range(self.rows()):
      for col in range(self.cols()):
        yield row, col, self[row, col]

  def rows(self):
    return self._rows

  def cols(self):
    return self._cols
