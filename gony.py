#!/usr/bin/env python
# -*- coding: utf-8 -*

import re
import requests
from BeautifulSoup import BeautifulSoup

class Game:

  def __init__(self):
    self.firstq = list()
    self.secondq = list()
    self.thirdq = list()
    self.fourthq = list()
    self.currentq = self.firstq

  def add_event(self, event):
    self.currentq.append(event)

  def print_plays(self):
    for play in self.firstq:
      print play

class Play:

  def __init__(self, action, time, home_score, away_score):
    self.action = action
    self.time = time
    self.home_score = home_score
    self.away_score = away_score

  def __repr__(self):
    return ','.join((self.time, self.home_score, self.away_score, repr(self.action)))

class Action(object):

  def __init__(self, action_type):
    super(Action, self).__init__()
    self.action_type = action_type

class Event:

  def __init__(self, time, play, home_score, away_score):
    self.time = time
    self.play = play
    self.home_score = home_score
    self.away_score = away_score

  def string(self):
   return ','.join(self.time, self.play, self.score)

class Player:
  
  def __init__(self, name):
    self.name = name
    self.fga = 0
    self.fgm = 0
    self.tfga = 0
    self.tfgm = 0

  def madeThree(self):
    self.tfga = self.tfga + 1
    self.tfgm = self.tfgm + 1

  def missedThree(self):
    self.tfga = self.tfga + 1

  def missedTwo(self):
    self.fga = self.fga + 1

  def madeTwo(self):
    self.fga = self.fga + 1
    self.fgm = self.fgm + 1

  def __key(self):
    return (self.name)

  def __eq__(x, y):
    return x.__key() == y.__key()

  def __hash__(self):
    return hash(self.__key())

  def fg_line(self):
    return 'name', self.name, ': ', self.fgm, ' of ', self.fga

r = requests.get('http://espn.go.com/nba/playbyplay?gameId=320309015&period=0')

doc = r.text
soup = BeautifulSoup(doc)

play_rows = soup.findAll('tr', { "class" : ['even','odd'] })

events = list()

# parse html
for tag in play_rows:
  time = tag.find(style='text-align:center;').string
  play = tag.find(style='text-align:left;')
  if play is not None:
    if play.string is None:
      play = play.next.string
    else:
      play = play.string
  score = tag.find(nowrap=True)
  home_score = None
  away_score = None
  if score is not None:
    score = score.string
    m = re.match('(\d+)-(\d+)', score)
    home_score = m.group(1)
    away_score = m.group(2)

  if play is None and score is None:
    play = tag.td.nextSibling.next.string
  event = Event(time, play, home_score, away_score)
  events.append(event)

class Shot(Action):

  def __init__(self, shot_type, made, player, assist_player):
    super(Shot, self).__init__('shot')
    self.shot_type = shot_type
    self.made = made
    self.player = player
    self.assist_player = assist_player

  def __repr__(self):
    return ','.join((self.action_type, self.shot_type, repr(self.made), self.player, repr(self.assist_player)))

game = Game()

for event in events:
  m = re.match('(.*?) (makes|misses) (.*?)( \((.*?) assists\))?$', event.play)
  if m is not None:
    player = m.group(1)
    made_string = m.group(2)
    made = made_string is 'makes'
    shot_type = m.group(3)
    assist_player = None
    if len(m.groups()) is 5:
      assist_player = m.group(5)
    shot = Shot(shot_type, made, player, assist_player)
    play = Play(shot, event.time, event.home_score, event.away_score)
    game.add_event(play)

game.print_plays()

"""
players = dict()

for event in events:
  m = re.match('(.*?) (makes|misses) (.*?) \(.*? assists\)$', event.play)
  if m is not None and m.group(2)[0:10] == 'free throw':

  else:
    name = m.group(1)
    if name not in players:
      players[name] = Player(name)
    player = players[name]
    player.madeTwo()
    continue
  
  m = re.match('(.*?) misses (.*)$', event.play)
  if m is not None:
    print m.group(2)[0:10]
  if m is not None and m.group(2)[0:10] != 'free throw':
    name = m.group(1)
    if name not in players:
      players[name] = Player(name)
    player = players[name]
    player.missedTwo()
    continue
 
for player in players.values():
  print player.fg_line()
"""

