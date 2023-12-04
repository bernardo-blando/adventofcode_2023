import requests
import os
from dotenv import load_dotenv

load_dotenv()

COOKIE = os.getenv("COOKIE")
url = f'https://adventofcode.com/2023/day/2/input'
response = requests.get(url, headers={"Cookie": f"session={COOKIE}"})
input_data = response.text

# 12 red cubes, 13 green cubes, and 14 blue cubes

red_limit = 12
green_limit = 13
blue_limit = 14

input_data = input_data.split("\n")
input_data.remove(input_data[-1])

for x in range(len(input_data)):
  input_data[x] = input_data[x].replace(';', ',')
  input_data[x] = input_data[x].split(":")
  input_data[x][1] = input_data[x][1].split(",")

total = 0
total_power = 0

for y in range(len(input_data)):
  input_data[y][0] = int(input_data[y][0].split(" ")[1])
  good_game = True
  min_red = 0
  min_green = 0
  min_blue = 0

  for x in range(len(input_data[y][1])):
    input_data[y][1][x] = input_data[y][1][x].strip()
    input_data[y][1][x] = input_data[y][1][x].split(" ")
    input_data[y][1][x][0] = int(input_data[y][1][x][0])
    if input_data[y][1][x][1] == "red":

      if input_data[y][1][x][0] > min_red:
        min_red = input_data[y][1][x][0]
      if input_data[y][1][x][0] > red_limit:
        good_game = False

    elif input_data[y][1][x][1] == "green":

      if input_data[y][1][x][0] > min_green:
        min_green = input_data[y][1][x][0]
      if input_data[y][1][x][0] > green_limit:
        good_game = False

    elif input_data[y][1][x][1] == "blue":

      if input_data[y][1][x][0] > min_blue:
        min_blue = input_data[y][1][x][0]
      if input_data[y][1][x][0] > blue_limit:
        good_game = False

  if good_game:
    total += input_data[y][0]
  total_power += min_red * min_green * min_blue

print(total)
print(total_power)