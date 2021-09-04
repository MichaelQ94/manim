from math import floor
from manim import *
from pokercard import *
from grid import *
from equation_sequence import *

YOU_COLOR = GREEN
REST_COLOR = PURPLE
WIN_COLOR=ORANGE
LOSE_COLOR=BLUE
NUM_CARDS = 12
SLICE_ANGLE = TAU/NUM_CARDS
TEX_SCALE = 0.6
COLOR_MAP = {
      r"p_{win}": WIN_COLOR,
      r"p_{loss}": LOSE_COLOR,
      "your contribution": YOU_COLOR
    }

def last(list):
  return list[len(list)-1]

def set_color(tex):
  return tex.set_color_by_tex_to_color_map(COLOR_MAP)

def filename(card):
  return str(card) + ".png"

def initial_shift(card):
  return card.shift(5 * LEFT + 3 * UP)

def initial_cards():
  hearts = [ImageMobject(filename(card)).scale(0.5) for card in HEARTS]
  shifted = []
  prev = None
  for card in hearts:
    shifted_card = initial_shift(card) if prev == None else card.next_to(prev, RIGHT)
    shifted.append(shifted_card)
    prev = shifted_card
  return shifted

def s_text(text, **kwargs):
  return Text(text, **kwargs).scale(0.4)

def s_markup(text, **kwargs):
  return MarkupText(text, **kwargs).scale(0.4)

def s_mathtex(*args, **kwargs):
  return MathTex(*args, **kwargs).scale(0.75)

def s_tex(*args, **kwargs):
  return Tex(*args, **kwargs).scale(0.4)

def s_texm(*args, scale=TEX_SCALE, **kwargs):
  return TexMobject(*args, **kwargs).scale(scale)

def make_sector(shift, slices, **kwargs):
  return Sector(
    start_angle=shift*SLICE_ANGLE,
    angle=slices*SLICE_ANGLE,
    outer_radius=1,
    **kwargs)

def make_grid(rows, cols):
  side_length = 0.25
  grid = Grid(rows, cols)
  grid[0, 0] = Square(side_length).shift(0.5*LEFT + 2*UP)
  for i in range(0, grid.rows()):
    if i > 0:
      grid[i, 0] = Square(side_length).next_to(grid[i-1, 0], DOWN)

    for j in range(1, grid.cols()):
      grid[i, j] = Square(side_length).next_to(grid[i, j-1], RIGHT)
  return grid

def binomial(n, p):
  val = (1 - p)**n
  yield val
  for k in range(1, n+1):
    val = val * p * (n-k) / ((1 - p)*k)
    yield val

def make_bar_chart(num_trials, win_prob):
  values = [h for h in binomial(num_trials, win_prob)]
  mean = floor(num_trials * win_prob)
  bar_name_dict = {mean: mean, num_trials: num_trials}
  return BarChart(
    values,
    n_ticks=3,
    max_value=0.06,
    bar_names=[bar_name_dict.get(k, "") for k in range(0, num_trials+1)],
    bar_colors=[RED if k == mean else YELLOW for k in range(0, num_trials+1)])


class Poker(Scene):
  def play_wait(self, *args, **kwargs):
    self.play(*args, **kwargs)
    self.wait()

  def display_eq_seq(self, eq_seq):
    for m in eq_seq.mobjects():
      self.play_wait(FadeIn(m))
  
  def collapse_eq_seq(self, eq_seq):
    rhs = eq_seq.rhs()
    first_rhs = rhs[0].as_group()
    last_rhs = rhs[len(rhs)-1].as_group()

    last_rhs.generate_target()
    last_rhs.target.next_to(first_rhs, RIGHT)
    self.play_wait(*[FadeOut(r.as_group()) for r in rhs[1:-1]], MoveToTarget(last_rhs))
    del rhs[1:-1]

  def remove_last_rhs(self, *eq_seqs):
    for eq_seq in eq_seqs:
      del eq_seq.rhs()[-1]

  def construct(self):
    hearts = initial_cards()
    two_five = Group(*hearts[:4])
    six = hearts[4]
    seven_ace = Group(*hearts[5:])

    # show deck
    self.play_wait(*[FadeIn(card) for card in hearts])

    # deal cards
    self.play_wait(six.animate.shift(3*DOWN + LEFT), run_time=1)
    you_label = s_text("You").next_to(six, DOWN)
    card_back = ImageMobject("back.png").scale(0.5).align_to(six, RIGHT).shift(5.2*RIGHT)
    opp_label = s_text("Opponent").next_to(card_back, DOWN)

    self.play_wait(FadeIn(you_label))
    self.play_wait(FadeIn(card_back, opp_label))

    you = Group(six, you_label)
    opp = Group(card_back, opp_label)

    # show pot
    self.play_wait(you.animate.shift(2*LEFT), opp.animate.shift(2*RIGHT))

    pot = s_text("Pot: $50").shift(2.5*DOWN)
    self.play_wait(FadeIn(pot))

    # opponent bets
    bet = s_text("Bet: $25").move_to(opp.get_center() + 2.5*LEFT)
    self.play_wait(FadeIn(bet, shift=LEFT))

    # pose question
    question = s_text("Question: Is it a good idea to call this bet?").shift(1.5*UP)
    self.play_wait(FadeIn(question))
    self.play_wait(FadeOut(question))

    # determine win probability
    win_brace = Brace(two_five, color=WIN_COLOR)
    win_label = s_text("Win", color=WIN_COLOR).next_to(win_brace, DOWN)
    lose_brace = Brace(seven_ace, color=LOSE_COLOR)
    lose_label = s_text("Lose", color=LOSE_COLOR).next_to(lose_brace, DOWN)
    win = Group(win_brace, win_label)
    lose = Group(lose_brace, lose_label)
    win_slice = make_sector(3, 4, color=WIN_COLOR)
    lose_slice = make_sector(7, 8, color=LOSE_COLOR)
    win_loss_pie = Group(win_slice, lose_slice).move_to(opp.get_center())
    p_win = s_mathtex(r"p_{win}=\frac{1}{3}", color=WIN_COLOR).next_to(win_loss_pie, DOWN)
    p_lose = s_mathtex(r"p_{lose}=\frac{2}{3}", color=LOSE_COLOR).next_to(p_win, DOWN)
    win_loss = Group(win_loss_pie, p_win, p_lose)

    self.play_wait(FadeIn(win))
    self.play_wait(FadeIn(lose))
    self.play(FadeOut(opp))
    self.play_wait(FadeOut(win, lose), FadeIn(win_loss))

    # call bet
    call = s_text("Call: $25").move_to(you.get_center() + 2.5*RIGHT)
    self.play_wait(FadeIn(call, shift=RIGHT))

    # determine pot contribution percentage
    you_slice = make_sector(3, 3, color=YOU_COLOR)
    rest_slice = make_sector(6, 9, color=REST_COLOR)
    pot_pie = Group(you_slice, rest_slice).align_to(win_loss_pie, DOWN).shift(0.5*LEFT)
    total_pot = s_text("total pot: $100")
    your_contribution = s_text("your contribution: $25", color=YOU_COLOR)
    pot_breakdown = VGroup(total_pot, your_contribution) \
      .arrange(direction=DOWN, aligned_edge=LEFT) \
      .next_to(pot_pie, DOWN)
    pie_breakdown = Group(pot_pie, pot_breakdown)
    self.play_wait(
      FadeOut(call, target_position=pot_pie.get_center()),
      FadeOut(pot, target_position=pot_pie.get_center()),
      FadeOut(bet, target_position=pot_pie.get_center()),
      FadeIn(pie_breakdown))

    # move pie charts to left
    self.play_wait(
      FadeOut(you, two_five, seven_ace),
      pie_breakdown.animate.shift(5*LEFT + 2.75*UP - pot_pie.get_center()),
      win_loss.animate.shift(5*LEFT + 0.7*DOWN - win_loss_pie.get_center()))

    # 99 round scenario
    grid = make_grid(9, 11)
    grid_squares = Group(*[entry for (_, _, entry) in grid.entries()])
    grid_label = s_text("99 rounds").next_to(grid_squares, UP)
    grid_group = Group(grid_squares, grid_label)

    self.play_wait(FadeIn(grid_group))
    self.play_wait(*[
      entry.animate.set_stroke(WIN_COLOR).set_fill(color=WIN_COLOR, opacity=1)
      for (row, _, entry) in grid.entries()
      if row < 3])
    self.play_wait(*[
      entry.animate.set_stroke(LOSE_COLOR).set_fill(color=LOSE_COLOR, opacity=1)
      for (row, _, entry) in grid.entries()
      if row >= 3])
    
    self.play_wait(FadeOut(grid_group))
    
    # 99 round distribution
    win_loss_bar = make_bar_chart(99, 1/3).shift(2*RIGHT)
    win_count_label = s_text("# of wins").next_to(win_loss_bar, DOWN).shift(0.5*RIGHT)
    prob_label = s_text("probability").next_to(win_loss_bar, UP).shift(2.65*LEFT)
    bar_chart = Group(win_loss_bar, win_count_label, prob_label)
    self.play_wait(FadeIn(bar_chart))
    self.play_wait(FadeOut(bar_chart))

    # expected number of wins
    ex_wins = EquationSequence(lhs="expected wins", scale_factor=TEX_SCALE)
    ex_wins.add_rhs(
      r"$p_{win}$", r"$\times$", "(rounds)",
      transform=set_color)
    ex_wins.add_rhs(
      r"$\dfrac{1}{3}$", r"$\times 99$",
      transform=lambda tex : tex.set_color_by_tex("frac", WIN_COLOR))
    ex_wins.add_rhs("33")
    ex_wins.transform_group(lambda grp : grp.shift(LEFT + 2.5*UP))
    self.display_eq_seq(ex_wins)
    self.collapse_eq_seq(ex_wins)
    ex_wins_group = ex_wins.as_group()

    # profit per win
    win_profit = EquationSequence(lhs="profit per win", scale_factor=TEX_SCALE)
    win_profit.add_rhs(
      "(total pot)" , r"$-$", "(your contribution)",
      transform=set_color
    )
    win_profit.add_rhs(
      r"$100 - $", r"$25$",
      transform = lambda tex : tex.set_color_by_tex("25", YOU_COLOR)
    )
    win_profit.add_rhs("75")
    win_profit.transform_group(lambda grp : grp.next_to(ex_wins_group, DOWN).align_to(ex_wins_group, LEFT))
    self.display_eq_seq(win_profit)
    self.collapse_eq_seq(win_profit)
    win_profit_group = win_profit.as_group()

    # expected number of losses
    ex_losses = EquationSequence(lhs="expected losses", scale_factor=TEX_SCALE)
    ex_losses.add_rhs(
      r"$p_{loss}$", r"$\times$", "(rounds)",
      transform=set_color)
    ex_losses.add_rhs(
      r"$\dfrac{2}{3}$", r"$\times 99$",
      transform=lambda tex : tex.set_color_by_tex("frac", LOSE_COLOR))
    ex_losses.add_rhs("66")
    ex_losses.transform_group(lambda grp : grp.next_to(win_profit_group, DOWN).align_to(win_profit_group, LEFT))
    self.display_eq_seq(ex_losses)
    self.collapse_eq_seq(ex_losses)
    ex_losses_group = ex_losses.as_group()

    # profit per loss
    loss_profit = EquationSequence(lhs="profit per loss", scale_factor=TEX_SCALE)
    loss_profit.add_rhs(
      r"$-$", "(your contribution)",
      transform=set_color
    )
    loss_profit.add_rhs(
      r"$-25$",
      transform = lambda tex : tex.set_color_by_tex("25", YOU_COLOR)
    )
    loss_profit.transform_group(lambda grp : grp.next_to(ex_losses_group, DOWN).align_to(ex_losses_group, LEFT))
    self.display_eq_seq(loss_profit)
    self.collapse_eq_seq(loss_profit)
    loss_profit_group = loss_profit.as_group()

    base_eqs = Group(ex_wins_group, win_profit_group, ex_losses_group, loss_profit_group)

    # shift equations
    self.play_wait(
      FadeOut(pie_breakdown, shift=LEFT), FadeOut(win_loss, shift=LEFT),
      base_eqs.animate.shift(4.5*LEFT)
      )

    # expected profit
    total_profit = EquationSequence(lhs="total profit", scale_factor=TEX_SCALE)
    total_profit.add_rhs(
      "[(expected wins)",
      r"$\times$",
      "(profit per win)]",
      r"$+$",
      "[(expected losses)",
      r"$\times$",
      "(profit per loss)]"
    )
    total_profit.add_rhs(r"$33 \times 75 + 66 \times (-25)$")
    total_profit.add_rhs("825")
    total_profit.transform_group(lambda grp : grp.next_to(loss_profit_group, DOWN).align_to(loss_profit_group, LEFT))
    self.display_eq_seq(total_profit)
    self.collapse_eq_seq(total_profit)
    total_profit_group = total_profit.as_group()

    # profit per round
    avg_profit = EquationSequence(lhs="avg. profit", scale_factor=TEX_SCALE)
    avg_profit.add_rhs(r"$\dfrac{(\textrm{total profit})}{(\textrm{rounds})}$")
    avg_profit.add_rhs(r"$\dfrac{825}{99}$")
    avg_profit.add_rhs(str(round(825/99, 2)))
    avg_profit.transform_group(lambda grp : grp.next_to(total_profit_group, DOWN).align_to(total_profit_group, LEFT))
    self.display_eq_seq(avg_profit)
    self.collapse_eq_seq(avg_profit)

    def s_frac(*args, **kwargs):
      return MathTex(*args, **kwargs).scale(0.6)

    # show graph
    self.play_wait(FadeOut(
      ex_wins_group,
      win_profit_group,
      ex_losses_group,
      loss_profit_group,
      total_profit_group,
      avg_profit.as_group()))
    self.remove_last_rhs(ex_wins, win_profit, ex_losses, loss_profit, total_profit, avg_profit)

    # show ultimate goal
    goal_tex = Tex("Goal: avg. profit > 0").scale(0.6)
    goal = Group(goal_tex, SurroundingRectangle(goal_tex)).shift(3.5*UP)
    self.add(goal)
    self.wait()

    # derive general formula
    self.play_wait(FadeIn(
      ex_wins.as_group(),
      win_profit.as_group(),
      ex_losses.as_group(),
      loss_profit.as_group(),
      total_profit.as_group(),
      avg_profit.as_group()))
    avg_profit.add_rhs_mobject(
      s_frac(
        r"{[(\textrm{expected wins}) \times (\textrm{profit per win})] + [(\textrm{expected losses}) \times (\textrm{profit per loss})] \over (\textrm{rounds})}"
      )
    )
    avg_profit.add_rhs_mobject(
      s_frac(
        r"{",
        r"[",
        r"p_{win}",
        r"\times",
        r"(\textrm{rounds})",
        r"\times (\textrm{profit per win})] + [",
        r"p_{loss}",
        r"\times",
        r"(\textrm{rounds})",
        r"\times (\textrm{profit per loss})]",
        r"\over",
        r"(\textrm{rounds})",
        r"}") \
          .set_color_by_tex_to_color_map(COLOR_MAP)
    )
    for i in range (1, len(avg_profit.rhs())):
      self.play_wait(FadeIn(avg_profit.rhs()[i].as_group()))
    last_rhs = last(avg_profit.rhs())
    last_tex = last_rhs.get_tex()
    self.play_wait(last_tex.animate.set_color_by_tex("rounds", PURPLE))
    last_tex_simplified = MathTex(
      r"[",
      r"p_{win}",
      r"\times (\textrm{profit per win})] + [",
      r"p_{loss}",
      r"\times (\textrm{profit per loss})]"
    ).scale(TEX_SCALE).set_color_by_tex_to_color_map(COLOR_MAP).next_to(last_rhs.eq(), RIGHT)
    self.play_wait(TransformMatchingTex(last_tex, last_tex_simplified))
    last_rhs.set_tex(last_tex_simplified)

    # call out expected value
    ev_tex = Tex("Expected Value!").scale(0.8)
    ev_label = Group(ev_tex, SurroundingRectangle(ev_tex)).next_to(last_tex_simplified, RIGHT)
    self.play_wait(FadeIn(ev_label))
    self.play_wait(FadeOut(ev_label))

    last_tex = MathTex(
      r"[",
      r"p_{win}",
      r"\times ((\textrm{total pot}) -",
      r"\textrm{(your contribution)}",
      r")] + [",
      r"p_{loss}",
      r"\times (-",
      r"(\textrm{your contribution})",
      ")]"
    ).scale(TEX_SCALE).set_color_by_tex_to_color_map(COLOR_MAP)

    avg_profit.add_rhs_mobject(last_tex)
    self.play_wait(FadeIn(last(avg_profit.rhs()).as_group()))

    self.play(
      FadeOut(*[rhs.as_group() for rhs in avg_profit.rhs()[:-1]]),
      avg_profit.rhs()[-1].as_group().animate.next_to(avg_profit.lhs(), RIGHT))
    del avg_profit.rhs()[:-1]

    self.play_wait(
      FadeOut(ex_wins.as_group()),
      FadeOut(win_profit.as_group()),
      FadeOut(ex_losses.as_group()),
      FadeOut(loss_profit.as_group()),
      FadeOut(total_profit.as_group()),
      avg_profit.as_group().animate.shift(2.5*UP)
    )

    avg_profit.add_rhs_mobject(
      MathTex(
        r"[",
        r"p_{win}",
        r"\times ((\textrm{total pot}) -",
        r"\textrm{(your contribution)}",
        r")] + [(1 -",
        r"p_{win}",
        r") \times (-",
        r"(\textrm{your contribution})",
        ")]"
      ).scale(TEX_SCALE).set_color_by_tex_to_color_map(COLOR_MAP)
    )

    avg_profit.add_rhs_mobject(
      MathTex(
        r"[",
        r"p_{win}",
        r"\times (\textrm{total pot})",
        r"] - ",
        r"(\textrm{your contribution})"
      ).scale(TEX_SCALE).set_color_by_tex_to_color_map(COLOR_MAP)
    )

    for rhs in avg_profit.rhs()[1:]:
      self.play_wait(FadeIn(rhs.as_group()))

    goal_ineq = [
      MathTex(
        r"[",
        r"p_{win}",
        r"\times",
        r"(\textrm{total pot})",
        r"] - ",
        r"(\textrm{your contribution})",
        ">",
        "0",
      ).scale(TEX_SCALE).set_color_by_tex_to_color_map(COLOR_MAP),
      MathTex(
        r"p_{win}",
        r"\times",
        r"(\textrm{total pot})",
        ">",
        r"(\textrm{your contribution})",
      ).scale(TEX_SCALE).set_color_by_tex_to_color_map(COLOR_MAP),
      MathTex(
        r"p_{win}",
        ">",
        "{",
        r"(\textrm{your contribution})",
        r"\over",
        r"(\textrm{total pot})",
        "}"
      ).scale(TEX_SCALE).set_color_by_tex_to_color_map(COLOR_MAP)
    ]

    self.play_wait(FadeIn(goal_ineq[0]))

    for i in range(0, len(goal_ineq)-1):
      self.play_wait(TransformMatchingTex(goal_ineq[i], goal_ineq[i+1]))
    
    last_ineq = last(goal_ineq)

    self.play_wait(
      FadeOut(avg_profit.as_group()),
      last_ineq.animate.shift(2*UP),
      goal.animate.shift(0.5*DOWN))

    win_loss.move_to(DOWN + 3*LEFT)
    pie_breakdown.move_to(DOWN + 3*RIGHT).align_to(win_loss, UP)
    self.play_wait(FadeIn(win_loss, pie_breakdown))

    self.play_wait(
      FadeIn(Tex(r"\underline{Pot Odds}")),
      win_loss.animate.shift(LEFT),
      pie_breakdown.animate.shift(RIGHT)
    )

    self.wait(5)
