import requests
import os
from dotenv import load_dotenv
import numpy as np
import time as t 
load_dotenv()

COOKIE = os.getenv("COOKIE")
url = f'https://adventofcode.com/2023/day/10/input'
response = requests.get(url, headers={"Cookie": f"session={COOKIE}"})
input_data = response.text

ADJACENT = {
  'up': (-1, 0),
  'down': (1, 0),
  'left': (0, -1),
  'right': (0, 1)
}

compatibility = {
  '|': ['up', 'down'],
  '-': ['left', 'right'],
  'F': ['down', 'right'],
  '7': ['left', 'down'],
  'J': ['up', 'left'],
  'L': ['up', 'right'],
  'S': ['up', 'down', 'left', 'right'],
  '.': []
}

oposites = {
  'up': 'down',
  'down': 'up',
  'left': 'right',
  'right': 'left'
}

# with open('newtest.txt', 'r') as f:
#     input_data = f.read()

def parse_data(data):
    data = data.split('\n')
    data.pop()
    output = []
    for i in range(len(data)):
      output.append([char for char in data[i]])
    return np.array(output) 

def part1():
  def check_identical_lists(lst):
      for i in range(len(lst)):
          for j in range(i + 1, len(lst)):
              if lst[i] == lst[j]:
                  return True
      return False
  
  def discover_pipeline(grid, start):
      def open_cells(list):
          response = []
          for cell in list:
            for direction in compatibility[cell[2]]:
                direction_out_of_bounds = cell[0] + ADJACENT[direction][0] < 0 or cell[0] + ADJACENT[direction][0] >= len(grid) or cell[1] + ADJACENT[direction][1] < 0 or cell[1] + ADJACENT[direction][1] >= len(grid[0])
                new_cell = [cell[0] + ADJACENT[direction][0],
                            cell[1] + ADJACENT[direction][1],
                            grid[cell[0] + ADJACENT[direction][0]][cell[1] + ADJACENT[direction][1]]]
                
                is_compatible = oposites[direction] in compatibility[new_cell[2]] and not direction_out_of_bounds
                if is_compatible and new_cell not in closed:
                    response.append(new_cell)
            closed.append(cell)
          return response
      
      discovered_pipeline = np.zeros(grid.shape)

      loop_not_found = True
      closed = []
      open = {
        0:[[start[0], start[1], 'S']]
      }
      distance = 0
      while loop_not_found:
          cells = open_cells(open[distance])
          distance += 1
          for cell in cells:
              discovered_pipeline[cell[0]][cell[1]] = distance
          open[distance] = cells     
          if check_identical_lists(cells):
              return discovered_pipeline    


  def find_start(grid):
      for i in range(len(grid)):
          for j in range(len(grid[i])):
              if grid[i][j] == 'S':
                  return (i, j)
              
  start = find_start(input_data)
  pipeline = discover_pipeline(input_data, start)
  return pipeline, start

def part2():
  input_data[start[0]][start[1]] = '7'
  # make a copy of the pipeline but turn all values that are not 0 to 1
  new_pipeline = pipeline/pipeline
  #Change all nan values to 0
  new_pipeline = np.nan_to_num(new_pipeline)
  new_pipeline[start[0]][start[1]] = 1

  verticalCheck = new_pipeline.copy()
  horizontalCheck = new_pipeline.copy()

  for i in range(len(input_data)):
      for j in range(len(input_data[i])):
          if input_data[i][j] == '|':
              verticalCheck[i][j] = 0
          elif input_data[i][j] == '-':
              horizontalCheck[i][j] = 0
          elif input_data[i][j] in ["J", "L", "7", "F", "S"] and new_pipeline[i][j] == 1:
              verticalCheck[i][j] = 0.5
              horizontalCheck[i][j] = 0.5
  
  def count_consecutive_sublists(main_list, sub_lists):
    total_count = 0
    for sub_list in sub_lists:
        count = 0
        sub_len = len(sub_list)
        for i in range(len(main_list) - sub_len + 1):
            if np.array_equal(main_list[i:i + sub_len], sub_list):
                count += 1
        total_count += count
    return total_count

  area = 0
  for i in range(len(new_pipeline)):
      for j in range(len(new_pipeline[i])):
          if new_pipeline[i][j] == 0:

              above_values = input_data[:i, j][verticalCheck[:i, j] != 0]
              below_values = input_data[i+1:, j][verticalCheck[i+1:, j] != 0]
              left_values = input_data[i, :j][horizontalCheck[i, :j] != 0]
              right_values = input_data[i, j+1:][horizontalCheck[i, j+1:] != 0]
              
              right_count = horizontalCheck[i, j+1:].sum()
              left_count = horizontalCheck[i, :j].sum()
              above_count = verticalCheck[:i, j].sum()
              below_count = verticalCheck[i+1:, j].sum()

              above_penaly = count_consecutive_sublists(above_values, [['F', 'L'],['7', 'J']])
              above_count = above_count - above_penaly

              below_penaly = count_consecutive_sublists(below_values, [['F', 'L'],['7', 'J']])
              below_count = below_count - below_penaly

              left_penaly = count_consecutive_sublists(left_values, [['L', 'J'],['F', '7']])
              left_count = left_count - left_penaly

              right_penaly = count_consecutive_sublists(right_values, [['L', 'J'],['F', '7']])
              right_count = right_count - right_penaly
   
              if above_count % 2 == 1 and below_count % 2 == 1 and left_count % 2 == 1 and right_count % 2 == 1:
                  area += 1
  return area
  

def print_grid(grid):
  for i in range(len(grid)):
    for j in range(len(grid[i])):
      print(str(grid[i][j])+ ' ', end='')
    print()
  print('\n')


input_data = parse_data(input_data)
pipeline, start = part1()

print("part1:", int(np.max(pipeline)))

print("part2:", part2()) 






