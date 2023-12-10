import requests
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()

COOKIE = os.getenv("COOKIE")
url = f'https://adventofcode.com/2023/day/9/input'
response = requests.get(url, headers={"Cookie": f"session={COOKIE}"})
input_data = response.text


# with open("input.txt", "r") as f:
#     input_data = f.read()

def parse_input(input_data):
    result = input_data.split("\n")
    del result[-1]
    result = np.array([x.split(" ") for x in result])
    result= result.astype(int)
    return result

def part1(input_data):
    
  totals = []
  total_firsts = []
  for row in input_data:
    piramide = []
    piramide.append(row)

    while True:
      row = np.diff(row)
      piramide.append(row)
      if np.sum(row) == 0:
        break
    
    total = 0
    total_first = 0
    last_value = 0

    for i in range(len(piramide)):
      total += piramide[i][-1]    
    totals.append(total)

    inverted = np.flip(piramide)
    for i in range(len(inverted)):
      total_first = inverted[i][0] - last_value
      last_value = total_first

    total_firsts.append(total_first)
    
  print(np.sum(totals))
  print(np.sum(total_firsts))


input_data = parse_input(input_data)

part1(input_data)    
