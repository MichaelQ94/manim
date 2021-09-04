from typing import List

class CardValue:
  def __init__(self, values: List[int]):
    self._values = values
  
  def values(self):
    return self._values

  def highest(self):
    highest = 0;
    for value in self.values():
      if value > highest:
        highest = value
    
    return highest
  
  def __str__(self):
    if len(self.values()) > 1:
      return "A"
    
    value = self.values()[0]
    if value >= 2 and value <= 10:
      return str(value)
    elif value == 11:
      return "J"
    elif value == 12:
      return "Q"
    elif value == 13:
      return "K"
    else:
      raise ValueError('Invalid card value %s' % value)
  
ACE = CardValue([1, 14])
TWO = CardValue([2])
THREE = CardValue([3])
FOUR = CardValue([4])
FIVE = CardValue([5])
SIX = CardValue([6])
SEVEN = CardValue([7])
EIGHT = CardValue([8])
NINE = CardValue([9])
TEN = CardValue([10])
JACK = CardValue([11])
QUEEN = CardValue([12])
KING = CardValue([13])
ALL_VALUES = [TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE]

class PokerSuit:
  def __init__(self, suit):
    self._suit = suit
  
  def __str__(self):
    return self._suit

HEART = PokerSuit("H")
DIAMOND = PokerSuit("D")
SPADE = PokerSuit("S")
CLUB = PokerSuit("C")

class PokerCard:
  def __init__(self, value, suit):
    self._value = value
    self._suit = suit
  
  def value(self):
    return self._value
  
  def suit(self):
    return self._suit

  def __str__(self):
    return str(self.value()) + str(self.suit())

HEARTS = [PokerCard(value, HEART) for value in ALL_VALUES]
