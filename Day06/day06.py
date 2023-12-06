import requests
import os
from dotenv import load_dotenv
load_dotenv()



def find_wining_values(maxX, y):
  results = []
  for wait in range(maxX):
      b = -wait
      speed = -b
      d = speed*(maxX + b)
      if d > y:
          results.append((wait))
  return results
        







COOKIE = os.getenv("COOKIE")
url = f'https://adventofcode.com/2023/day/6/input'
response = requests.get(url, headers={"Cookie": f"session={COOKIE}"})
input_data = response.text

# with open("data.txt", "r") as f:
#   input_data = f.read()

separator = "\n"
time, distance, extra = input_data.split(separator)

time = time.split()
distance = distance.split()


time.pop(0)
distance.pop(0)

time = [int(i) for i in time]
distance = [int(i) for i in distance]

total_scores = []

for i in range(len(time)):
  if time[i] == None or distance[i] == None:
    continue
  total_scores.append(find_wining_values(time[i], distance[i]))

len_results = [len(i) for i in total_scores]
print(len_results)

total_error = 1
for i in range(len(len_results)):
  total_error = total_error * len_results[i]

print(total_error)
print(input_data)