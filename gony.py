#!/usr/bin/env python
# -*- coding: utf-8 -*

import re
import requests
from BeautifulSoup import BeautifulSoup

class Event:

  def __init__(self, time, play, score):
    self.time = time
    self.play = play
    self.score = score

  def string(self):
   return self.time, self.play, self.score

class Player:
  
  def __init__(self, name):
    self.name = name
    self.fga = 0
    self.fgm = 0

  def missed(self):
    self.fga = self.fga + 1

  def made(self):
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

r = requests.get('http://scores.espn.go.com/nba/playbyplay?gameId=320226031&period=0')

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
  if score is not None:
    score = score.string
  if play is None and score is None:
    play = tag.td.nextSibling.next.string
  event = Event(time, play, score)
  events.append(event)

players = dict()

for event in events:
  m = re.match('(.*?) makes (.*)$', event.play)
  if m is not None and m.group(2)[0:10] != 'free throw':
    name = m.group(1)
    if name not in players:
      players[name] = Player(name)
    player = players[name]
    player.made()
    continue
  
  m = re.match('(.*?) misses (.*)$', event.play)
  if m is not None:
    print m.group(2)[0:10]
  if m is not None and m.group(2)[0:10] != 'free throw':
    name = m.group(1)
    if name not in players:
      players[name] = Player(name)
    player = players[name]
    player.missed()
    continue
 
for player in players.values():
  print player.fg_line()
