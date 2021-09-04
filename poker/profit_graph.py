from manim import *
import random

WIN = 'W'
LOSS = 'L'
WIN_LOSS_LIST = ([WIN]*33) + ([LOSS]*66)
WIN_PROFIT = 75
LOSS_PROFIT = -25

def get_profit(result):
  return WIN_PROFIT if result == WIN else LOSS_PROFIT

def s_tex(*args, **kwargs):
  return Tex(*args, **kwargs).scale(0.6)

def fischer_yates(list):
  for i in range(len(list)):
    index = random.randrange(i, len(list))
    val = list[i]
    list[i] = list[index]
    list[index] = val
  return list

class Profit(Scene):
  def construct(self):
    plane = Axes(
      x_range=(0, 100, 10),
      y_range=(-300, 1200, 100),
      x_length=9,
      y_length=6,
      axis_config={
        "include_numbers": True,
        "number_scale_value": 0.6
      },
    )

    plane.center()
    win_loss_sequence = fischer_yates(WIN_LOSS_LIST)
    total = 0
    profit = [0]
    for i in range(0, 99):
      total += get_profit(win_loss_sequence[i])
      profit.append(total)

    line_graph = plane.get_line_graph(
      x_values=[i for i in range(0, 100)],
      y_values=profit,
      stroke_width=1,
      line_color=WHITE,
      vertex_dot_radius=0.02
    )
    
    x_label = plane.get_x_axis_label(s_tex("rounds"), edge=DOWN, direction=DOWN) \
      .shift(0.25*DOWN)
    y_label = plane.get_y_axis_label(s_tex("profit (cumulative)"), edge=UP, direction=UP) \
      .shift(0.4*RIGHT)

    self.play(FadeIn(plane, line_graph, x_label, y_label))
    self.wait(1)

    avg_line = plane.get_line_graph(
      x_values=[0, 99],
      y_values=[0, total],
      vertex_dot_radius=0.05
    )

    self.play(FadeIn(avg_line))
    self.wait(1)

    label = s_tex(
      "slope = ",
      r"$\dfrac{\textrm{(total profit)}}{\textrm{(rounds)}}$",
      "= avg. profit").shift(2*UP)
    arrow = Arrow(
      stroke_width=1,
      max_tip_length_to_length_ratio=0.1,
      start=label.get_bottom(),
      end=label.get_bottom() + 2*DOWN)
    self.play(FadeIn(label, arrow))
    self.wait(1)

    goal_tex = s_tex("Goal: avg. profit > 0")
    goal = Group(goal_tex, SurroundingRectangle(goal_tex)).shift(3.5*UP)
    self.play(FadeIn(goal))
    self.wait(1)

    self.play(FadeOut(plane, line_graph, avg_line, x_label, y_label, label, arrow))
    self.wait(2)
