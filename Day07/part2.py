import requests
import os
from dotenv import load_dotenv

load_dotenv()

CARD_ORDER=['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']
RANK_ORDER=['hc', '2k', '2*2k', '3k', 'fh', '4k', '5k']


def order_by_rank(hands):
  new_hands = []
  for hand in hands:
    high_card_score = ''
    for i in range(len(hand[0])):
      order_value = CARD_ORDER.index(hand[0][i])+1
      high_card_score = high_card_score + f"{order_value:02d}"
    rank_value = str(RANK_ORDER.index(get_rank(hand[0]))+1)
    final_hand_score = rank_value + high_card_score
    hand.append(int(final_hand_score))
    new_hands.append(hand)
    new_hands.sort(key=lambda x: x[2], reverse=False)

  return new_hands

def get_rank(hand):
  freq = {}
  for card in hand:
    if card in freq:
      freq[card] += 1
    else:
      freq[card] = 1

  nj = freq.get('J', 0)
  freq.pop('J', None)

  if nj > 0 and nj < 5:
    replace_key = max(freq, key=freq.get)
    hand = hand.replace('J', replace_key)

  new_freq = {}
  for card in hand:
    if card in new_freq:
      new_freq[card] += 1
    else:
      new_freq[card] = 1

  if 5 in new_freq.values():
    return '5k'
  elif 4 in new_freq.values():
    return '4k'
  elif 3 in new_freq.values() and 2 in new_freq.values():
    return 'fh'
  elif 3 in new_freq.values():
    return '3k'
  elif 2 in new_freq.values() and len(new_freq.values()) == 3:
    return '2*2k'
  elif 2 in new_freq.values():
    return '2k'
  else:
    return 'hc'

# COOKIE = os.getenv("COOKIE")
# url = f'https://adventofcode.com/2023/day/7/input'
# response = requests.get(url, headers={"Cookie": f"session={COOKIE}"})
# input_data = response.text

with open('data.txt', 'r') as f:
  input_data = [h.strip().split(' ') for h in f.readlines()]

ordered_hands = order_by_rank(input_data)
total_winnings = 0
for i in range(1, len(ordered_hands)+1):
  total_winnings += i*int(ordered_hands[i-1][1])
  # print(f"Multiplier: {i}, Hand: {ordered_hands[i-1][0]}, Score: {ordered_hands[i-1][2]}, Total: {total_winnings}")
  

print(total_winnings)