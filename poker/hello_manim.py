from manim import *


class Hello(Scene):
  def construct(self):
    tex = MathTex(r"(pot + bet) \times p + -(call) \times (1 - p)")

    self.play(Write(tex))
    self.wait()