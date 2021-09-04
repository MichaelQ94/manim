from manim import *

def identity(x):
  return x

class Rhs():
  def __init__(self, eq, tex):
    self._eq = eq
    self._tex = tex
  
  def get_tex(self):
    return self._tex

  def set_tex(self, tex):
    self._tex = tex
  
  def eq(self):
    return self._eq

  def as_group(self):
    return Group(self._eq, self._tex)

class EquationSequence:
  def __init__(self, lhs, scale_factor):
    self._scale_factor = scale_factor
    self._lhs = self._s_tex(lhs)
    self._rhs = []

  def add_rhs(self, *args, transform=identity): 
    self._rhs.append(self._make_rhs(*args, transform=transform))

  def add_rhs_mobject(self, mobject):
    eq = self._s_tex("=")
    self._rhs.append(self._position_rhs(Rhs(eq, mobject.next_to(eq, RIGHT))))


  def lhs(self):
    return self._lhs
  
  def rhs(self):
    return self._rhs
  
  def transform_group(self, transform):
    transform(Group(*[m for m in self.mobjects()]))

  def mobjects(self):
    yield self._lhs
    for rhs in self.rhs():
      yield rhs.as_group()

  def as_group(self):
    return Group(*[m for m in self.mobjects()])
  
  def _make_rhs(self, *args, transform):
    eq = self._s_tex("=")
    return self._position_rhs(Rhs(eq, self._s_tex(*args, transform=transform).next_to(eq, RIGHT)))

  def _position_rhs(self, rhs):
    if len(self._rhs) == 0:
      rhs.as_group().next_to(self._lhs, RIGHT)
    else:
      prev = self._rhs[-1].as_group()
      rhs.as_group().next_to(prev, DOWN).align_to(prev, LEFT)
    return rhs
  
  def _s_tex(self, *args, transform=identity):
    return transform(Tex(*args).scale(self._scale_factor))
