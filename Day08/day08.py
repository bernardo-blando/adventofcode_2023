import requests
import os
from dotenv import load_dotenv
from math import lcm
load_dotenv()

COOKIE = os.getenv("COOKIE")
url = f'https://adventofcode.com/2023/day/8/input'
response = requests.get(url, headers={"Cookie": f"session={COOKIE}"})
input_data = response.text


data = [x.split("=") for x in input_data.split("\n") if x.strip()]
commands = data.pop(0)[0]
state_transitions = {}

for x in range(len(data)):
  data[x][0] = data[x][0].strip()
  data[x][1] = data[x][1].strip()
  data[x][1] = (data[x][1][1:4], data[x][1][6:9])
  state_transitions[data[x][0]] = data[x][1]

#part1
def part1():
  count = 0
  state = "AAA"

  while state != "ZZZ":
    for letter in commands:
      count += 1
      if letter == "L":
        state = state_transitions[state][0]
      if letter == "R":
        state = state_transitions[state][1]
      if state == "ZZZ":
        break

  print(count)

# Part 2
def part2():
  def find_regularity(start):
    steps = 0
    state = start
    answers = []
    while len(answers) < 10:
      for letter in commands:
        steps += 1
        if letter == "L":
          state = state_transitions[state][0]
        if letter == "R":
          state = state_transitions[state][1]
        if state[2] == "Z":
          answers.append(steps)
          steps=0
          
    return answers

  start_points = [x for x in state_transitions.keys() if x[2] == "A"]
  list = []
  for start in start_points:
    # print(start, find_regularity(start))
    list.append(find_regularity(start)[0])
  result = lcm(list[0], list[1], list[2], list[3], list[4], list[5])
  print(result)

part1()
part2()