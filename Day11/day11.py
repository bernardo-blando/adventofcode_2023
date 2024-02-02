import numpy as np

with open('input.txt', 'r') as f:
    input_data = f.read()

def parse_data(data):
    data = data.split('\n')
    data.pop()
    output = [] 
    o=1
    for i in range(len(data)):
      row = []
      for char in data[i]:
        if char == '.':
          row.append(0)
        else:
          row.append(o)
          o += 1
      output.append(row)
    return np.array(output)

def expand_universe(light):

  def get_keys(input):
    response = []
    for row in range(len(input)):
      if input[row].sum() ==0:
        response.append(row)     
    return response

  empty_rows = get_keys(light)
  empty_cols = get_keys(light.transpose())
  expanded_rows = np.insert(light, empty_rows, 0, axis=0)
  expanded = np.insert(expanded_rows, empty_cols, 0, axis=1)

  return expanded

def get_galaxies_coordenates(uni):
  galaxies={}
  for i in range(len(uni)):
    for o in range(len(uni[i])):
      value = uni[i, o]
      if value != 0:
        galaxies[value] = (i, o)
  return galaxies

def get_distance(a, b):
  distance = abs(a[0]-b[0])+abs(a[1]-b[1])
  return distance

def galaxy_sum(galaxy, gals_left):
  print("Gals left:", gals_left)
  gal_sum =0
  for gal in gals_left.values():
    gal_sum += get_distance(galaxy, gal)

  return gal_sum


observed = parse_data(input_data)
universe = expand_universe(observed)
galaxies = get_galaxies_coordenates(universe)
total = 0
gal_copy = galaxies.copy()

for key, galaxy in galaxies.items():
  print("Galaxy n", key)
  gal_copy.pop(key)
  gal_sum = galaxy_sum(galaxy, gal_copy)
  print("Sum ", gal_sum)
  total += gal_sum
print("\nThe grand total: ",total)