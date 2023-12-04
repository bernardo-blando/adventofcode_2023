import requests
import os
from dotenv import load_dotenv
import re
import numpy as np
load_dotenv()

COOKIE = os.getenv("COOKIE")
url = f'https://adventofcode.com/2023/day/4/input'
response = requests.get(url, headers={"Cookie": f"session={COOKIE}"})
input_data = response.text

cards = input_data.split("\n")
cards.remove("")
copycards = []
def clean_cards(cards):
  for n in range(len(cards)):
    cards[n] = re.split(":|\|", cards[n])
    cards[n] = [x.strip() for x in cards[n]]
    cards[n] = [x.split(" ") for x in cards[n]]
    for y, part in enumerate(cards[n]):
      cards[n][y] = list(filter(lambda x: x != "" and x != " ", part))
    cards[n][0]= int(cards[n][0][1])
  return cards

def count_matches(cards, matches = []):
  card_multiplier = {int(index): 1 for index in range(1, len(cards)+1)}
  for card in cards:
    card_matches=0
    for x in card[1]:
      if x in card[2]:
        card_matches+=1
    if card_matches > 0: 
      for x in range(card[0]+1, card[0]+1+card_matches):
        if x > 203:
          continue
        card_multiplier[x] += card_multiplier[card[0]]
      
  
    matches.append(card_matches)

  return matches, card_multiplier

cards = clean_cards(cards)
matches, multiplier = count_matches(cards)

total = 0

for y, x in enumerate(matches):
    if x>0:
      total += (2**(x-1))
print("Total: ", total)

sum = sum(multiplier.values())
print("Number of cards: ",sum)