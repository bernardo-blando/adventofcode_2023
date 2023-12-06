import requests
import os
from dotenv import load_dotenv
import pandas as pd
import math
import numpy as np
class Type:
  def __init__(self, type, values):
    self.type = type
    self.values = values

class Function:
  """
  Non linear function defined by a set of intervals
  Input: List of lists describing the intervals and the y values of the function. [[start, stop, y], [start, stop, y], ...]
  """
  def __init__(self, intervals):
    self.intervals = intervals


  def interval_response(self, start, stop):
    """
    Returns the response of the function for the input interval.
    Output: List of lists describing the funcions response for the input interval.
    """
    response = []
    for i in range(len(self.intervals)):
      if self.intervals[i][0] >= start and self.intervals[i][1] <= stop:
        response.append([self.intervals[i][0], self.intervals[i][1], self.intervals[i][2]])
      elif self.intervals[i][0] >= start and self.intervals[i][0] < stop:
        response.append([self.intervals[i][0], stop, self.intervals[i][2]])
      elif self.intervals[i][1] > start and self.intervals[i][1] <= stop:
        response.append([start, self.intervals[i][1], self.intervals[i][2]])
      elif self.intervals[i][0] < start and self.intervals[i][1] > stop:
        response.append([start, stop, self.intervals[i][2]])
    return response
  
  def fill_interval_gaps(self):
    """
    Updates the intervals of the function by filling the gaps between them with [start, stop, 0]
    Output: None
    """
    response = []
    for i in range(len(self.intervals)-1):
      response.append([self.intervals[i][1]+1, self.intervals[i+1][0]-1, 0])
    self.intervals = self.intervals + response
    self.intervals = sorted(self.intervals, key=lambda x: x[0])

  def response(self, x):
    """
    Returns the response of the function for the input x.
    Output: An int: the input x added to y
    """
    for i in self.intervals:
      if x >= i[0] and x <= i[1]:
        return x+i[2]
    return None
  
  def lowest_response_for_interval(self, start, stop):
    """
    Returns the lowest response of the function for the input interval.
    Output:INT The lowest input+y value)
    """
    response = self.interval_response(start, stop)
    response = sorted(response, key=lambda x: x[2])
    return response[0][2]+response[0][0]
 

  def composite_function(self, other):
    """
    Returns the composite function of self and other.
    Output: A new Function object describing the composite function. 
    """
    response = []
    # print("Self intervals", self.intervals)
    # print("Other intervals", other.intervals)
    for i in other.intervals:
      afected_interval = [i[0]+i[2], i[1]+i[2]]
      # print("Afected interval", afected_interval)
      self_function_response = self.interval_response(afected_interval[0], afected_interval[1])
      # print("Self function response", self_function_response)
      for j in self_function_response:
        response.append([j[0]-i[2], j[1] -i[2], j[2]+i[2]])

    #sort response
    response = sorted(response, key=lambda x: x[0])

    return Function(response)
    
def find_function(data, response=[]):
  df = pd.DataFrame(data, columns=['destination', 'source', 'range'])
  df = df.sort_values('source')
  response.append([-math.inf, df['source'].min() -1, 0])
  for i in range(len(data)):
    start = df.iloc[i]['source']
    stop = df.iloc[i]['source']+df.iloc[i]['range']-1
    operation = df.iloc[i]['destination']- df.iloc[i]['source']
    response.append([start, stop, operation])
  response.append([response[-1][1]+1, math.inf, 0])
  return response
    

load_dotenv()

COOKIE = os.getenv("COOKIE")
url = f'https://adventofcode.com/2023/day/5/input'
response = requests.get(url, headers={"Cookie": f"session={COOKIE}"})
input_data = response.text

# print(input_data)

# with open('data.txt', 'r') as f:
#   input_data = f.read()

input_data = input_data.split('\n\n')
for i in range(len(input_data)):
  input_data[i] = input_data[i].split('\n')

input_data[-1].pop(-1)

seeds = input_data.pop(0)
seeds = seeds[0].split(' ')
seeds = seeds[1:]
seeds= [int(i) for i in seeds]
seeds = Type('seed', seeds)

data = {}
for i in range(len(input_data)):
  input_data[i][0] = input_data[i][0][0:-5]
  data[input_data[i][0]] = [x.split(' ') for x in input_data[i][1:]]
  data[input_data[i][0]] = [[int(x) for x in y] for y in data[input_data[i][0]]]

functions = []
for key, val in data.items():
  functions.append(Function(find_function(val, response=[])))

print("Function  0",functions[0].intervals)
print("Function 1:", functions[1].intervals)
print("Function 2:", functions[2].intervals)
print("Function 3:", functions[3].intervals)
print("Function 4:", functions[4].intervals)
print("Function 5:", functions[5].intervals)
print("Function 6:", functions[6].intervals)

final_function = functions[1].composite_function(functions[0])
print("Final Function: 1 o 0", final_function.intervals)

final_function = functions[2].composite_function(final_function)
print("Final Function: 2 o 1 o 0", final_function.intervals)

final_function = functions[3].composite_function(final_function)
print("Final Function: 3 o 2 o 1 o 0", final_function.intervals)

final_function = functions[4].composite_function(final_function)
print("Final Function: 4 o 3 o 2 o 1 o 0", final_function.intervals)

final_function = functions[5].composite_function(final_function)
print("Final Function: 5 o 4 o 3 o 2 o 1 o 0", final_function.intervals)

final_function = functions[6].composite_function(final_function)

final_function.fill_interval_gaps()

print("Final Function: 6 o 5 o 4 o 3 o 2 o 1 o 0", final_function.intervals)



new_seeds = []
#group seed values in pairs by order
for i in range(0, len(seeds.values), 2):
  new_seeds.append([seeds.values[i], seeds.values[i+1]])

print("New seeds", new_seeds)

lowest_values = []
for i in new_seeds:
  print("Seed pair", i)
  lowest_values.append(final_function.lowest_response_for_interval(i[0], i[1]+i[0]))
  print("Lowest value of the pair", lowest_values[-1])

print("LOWEST VALUE", min(lowest_values))

print()