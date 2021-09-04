from manim import *

NUM_CARDS = 12
SLICE_ANGLE = TAU/NUM_CARDS

def make_sector(n):
  return Sector(
    start_angle=((n + (NUM_CARDS / 4)) % NUM_CARDS) * SLICE_ANGLE,
    angle=SLICE_ANGLE,
    outer_radius=1.5,
    stroke_width=2,
    stroke_color=BLUE,
    fill_color=BLACK)

class Main(Scene):
  def construct(self):
    sectors = [make_sector(n) for n in range(NUM_CARDS)]
    self.play(*[Create(s) for s in sectors])
    self.wait()
    self.play(*[FadeToColor(s, color=ORANGE) for s in sectors[:4]])
    self.wait()
    self.play(*[FadeToColor(s, color=BLUE) for s in sectors[4:]])
    self.wait(2)