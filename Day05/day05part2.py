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
  
  def interval_response_v2(self, start, stop):
    """
    Returns the response of the function for the input interval.
    Output: List of lists describing the function's response for the input interval.
    """
    response = []
    for i in range(len(self.intervals)):

      # Check if the interval is completely within the input interval
      if self.intervals[i][0] >= start and self.intervals[i][1] <= stop:
        print("Case 1", self.intervals[i], "vs", [start, stop])
        response.append([self.intervals[i][0]+ self.intervals[i][2], self.intervals[i][1] + self.intervals[i][2]])

      # Check if the interval starts within the input interval but ends outside
      elif (self.intervals[i][0] >= start and self.intervals[i][0] <= stop) and self.intervals[i][1] > stop:
        print("Case 2", self.intervals[i], "vs", [start, stop])
        response.append([self.intervals[i][0]+self.intervals[i][2], stop+self.intervals[i][2]])

      # Check if the interval ends within the input interval but starts outside
      elif self.intervals[i][0] < start and self.intervals[i][1] >= start and self.intervals[i][1] <= stop:
        print("Case 3", self.intervals[i], "vs", [start, stop])
        response.append([start+self.intervals[i][2], self.intervals[i][1]+self.intervals[i][2]])

      # Check if the interval starts before the input interval and ends after
      elif self.intervals[i][0] < start and self.intervals[i][1] > stop:
        print("Case 4", self.intervals[i], "vs", [start, stop])
        response.append([start+self.intervals[i][2], stop+self.intervals[i][2]])

    return response
    
  
  def fill_interval_gaps(self):
    """
    Updates the intervals of the function by filling the gaps between them with [start, stop, 0]
    Output: None
    """
    #Ensure that self.intervals is sorted
    self.intervals = sorted(self.intervals, key=lambda x: x[0])

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
    for i in other.intervals:
      affected_start = min(i[0], i[1])
      affected_stop = max(i[0], i[1])
      self_function_response = self.interval_response(affected_start, affected_stop)
      for j in self_function_response:
        response.append([j[0] - i[2], j[1] - i[2], j[2] + i[2]])

    # Sort response
    response = sorted(response, key=lambda x: x[0])

    return Function(response)

  def remove_negative_intervals(self):
    """
    Removes the intervals with negative y values.
    Output: None
    """
    response = []
    for i in self.intervals:
      if i[1] > i[0]:
        response.append(i)
    self.intervals = response
    
def find_function(data):
  response=[]
  df = pd.DataFrame(data, columns=['destination', 'source', 'range'])
  df = df.sort_values('source')
  response.append([-math.inf, df['source'].min() -1, 0])
  for i in range(len(data)):
    start = df.iloc[i]['source']
    stop = df.iloc[i]['source']+df.iloc[i]['range']-1
    operation = df.iloc[i]['destination']- df.iloc[i]['source']
    response.append([start, stop, operation])
  response.sort(key=lambda x: x[0])
  response.append([response[-1][1]+1, math.inf, 0])
  return response
    
def clean_data(input_data):
  input_data = input_data.split('\n\n')
  input_data = [group.split('\n') for group in input_data]
  input_data[-1].pop(-1)

  seeds = input_data.pop(0)[0].split()[1:]
  seeds = [int(seed) for seed in seeds]

  data = {}
  for group in input_data:
    key = group[0][:-5]
    values = [list(map(int, item.split())) for item in group[1:]]
    data[key] = values

  new_seeds = [seeds[i:i+2] for i in range(0, len(seeds), 2)]

  return data, new_seeds

load_dotenv()

COOKIE = os.getenv("COOKIE")
url = f'https://adventofcode.com/2023/day/5/input'
response = requests.get(url, headers={"Cookie": f"session={COOKIE}"})
input_data = response.text

print(input_data)

# with open('data.txt', 'r') as f:
#   input_data = f.read()

data, seeds = clean_data(input_data)

functions={}
for key in data.keys():
  functions[key] = Function(find_function(data[key]))

seeds = [[x[0], x[1] + x[0]-1] for x in seeds]

print("Seeds1", seeds)
for name, function in functions.items():
  print(name, function.intervals)
  results_for_function = []
  for seed in seeds:
    print("Seed", seed)
    seed_result = function.interval_response_v2(seed[0], seed[1])
    results_for_function.extend(seed_result)

  sorted_results = sorted(results_for_function, key=lambda x: x[0])  
  print("Results for function", name, sorted_results)

  seeds = sorted_results





print(seeds[0][0])