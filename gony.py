#!/usr/bin/env python
# -*- coding: utf-8 -*

import re
import requests
from BeautifulSoup import BeautifulSoup

r = requests.get('http://scores.espn.go.com/nba/playbyplay?gameId=320226031&period=0')

doc = r.text
soup = BeautifulSoup(doc)

play_rows = soup.findAll('tr', { "class" : ['even','odd'] })

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
  print time, play, score
  
