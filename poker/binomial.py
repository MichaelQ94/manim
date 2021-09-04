from manim import *

def binomial(n, p):
  val = (1 - p)**n
  yield val
  for k in range(1, n+1):
    val = val * p * (n-k) / ((1 - p)*k)
    yield val

class Main(Scene):
  def construct(self):
    values = [h for h in binomial(99, 1/3)]
    win_loss_bar = BarChart(
      values,
      max_value=max(values),
      bar_names=["33" if k == 33 else "" for k in range(0, 100)],
      bar_colors=[ORANGE if k == 33 else BLUE for k in range(0, 100)])
    self.play(FadeIn(win_loss_bar))
    self.wait(2)