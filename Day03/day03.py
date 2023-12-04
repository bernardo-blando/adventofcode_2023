import requests
import os
from dotenv import load_dotenv
import numpy as np
load_dotenv()

COOKIE = os.getenv("COOKIE")
url = f'https://adventofcode.com/2023/day/3/input'
response = requests.get(url, headers={"Cookie": f"session={COOKIE}"})
input_data = response.text
print(input_data)

# with open('test.txt', 'r') as f:
#    input_data = f.read()

engines = input_data.split('\n')
engines.remove('')
print(engines)
symbol_coordinates = {}
number_coordinates = []

for row_index, row in enumerate(engines):
    previous_cell = ''
    for col_index, cell in enumerate(row):
      if cell != '.' and not cell.isdigit():
          symbol_coordinates.update( { (int(col_index), int(row_index)): cell } )
      elif cell.isdigit():
          if previous_cell.isdigit():
                  number_coordinates[-1][1] = number_coordinates[-1][1] + cell  
                  number_coordinates[-1][0].append((int(col_index), int(row_index)) )
          else:
            number_coordinates.append( [ [ (int(col_index), int(row_index)) ] , cell ] )
      previous_cell = cell

total = 0
found_symbol = False
gears= {}
gear_total = 0
# for each number coordinate check if there is a symbol in the surrounding 8 coordinates
for number in number_coordinates:
    print("number", number)
    if found_symbol:
        break
    for coordinate in number[0]:
        print("coordinate", coordinate)
        if found_symbol:
            break
        surrounding_coordinates = [(coordinate[0]+1, coordinate[1]), (coordinate[0]-1, coordinate[1]), (coordinate[0], coordinate[1]+1), (coordinate[0], coordinate[1]-1), (coordinate[0]+1, coordinate[1]+1), (coordinate[0]-1, coordinate[1]-1), (coordinate[0]+1, coordinate[1]-1), (coordinate[0]-1, coordinate[1]+1)]

        for surrounding_coordinate in surrounding_coordinates:
            print("Surrounding Coordinate",surrounding_coordinate)
            
            if surrounding_coordinate in symbol_coordinates:
                print("Found symbol")
                total += int(number[1])
                found_symbol = True
                if symbol_coordinates[(surrounding_coordinate[0], surrounding_coordinate[1])] == '*':
                  if (surrounding_coordinate[0], surrounding_coordinate[1])not in gears:
                    gears.update({(surrounding_coordinate[0], surrounding_coordinate[1]): int(number[1])})
                  else:
                    gear_total += gears[(surrounding_coordinate[0], surrounding_coordinate[1])] * int(number[1])
                    
    found_symbol = False
print("Total", total)

print("New total", gear_total)