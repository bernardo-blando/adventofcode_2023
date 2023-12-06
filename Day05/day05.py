import requests
import os
from dotenv import load_dotenv

class Type:
  def __init__(self, type, values):
    self.type = type
    self.values = values



load_dotenv()

COOKIE = os.getenv("COOKIE")
url = f'https://adventofcode.com/2023/day/5/input'
response = requests.get(url, headers={"Cookie": f"session={COOKIE}"})
input_data = response.text

# print(input_data)

# with open('testing.txt', 'r') as f:
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

def convert(data, converter):
  result = []
  for i in data:
    found = False
    for j in converter:
      if i >= j[1] and i < j[1]+j[2]:
        result.append(i-j[1]+j[0])
        found = True
        break
    if not found:
      result.append(i)
  return result

print(data)
print("Seed to Soil")
print(seeds.values, data['seed-to-soil'])
seed_to_soil = convert(seeds.values, data['seed-to-soil'])
print("Soil to Fertilizer")
print(seed_to_soil, data['soil-to-fertilizer'])
soil_to_fertilizer = convert(seed_to_soil, data['soil-to-fertilizer'])
print("Fertilizer to Water")
print(soil_to_fertilizer, data['fertilizer-to-water'])
fertilizer_to_water = convert(soil_to_fertilizer, data['fertilizer-to-water'])
print("Water to Light")
print(fertilizer_to_water, data['water-to-light'])
water_to_light = convert(fertilizer_to_water, data['water-to-light'])
print("Light to Temperature")
print(water_to_light, data['light-to-temperature'])
light_to_temperature = convert(water_to_light, data['light-to-temperature'])
print("Temperature to Humidity")
print(light_to_temperature, data['temperature-to-humidity'])
temperature_to_humidity = convert(light_to_temperature, data['temperature-to-humidity'])
print("Humidity to Location")
print(temperature_to_humidity, data['humidity-to-location'])
humidity_to_location = convert(temperature_to_humidity, data['humidity-to-location'])

print("Seed values: ", seeds.values)
print("Results: ", humidity_to_location)
#print the lowest value in humidity_to_location
print("Lowest value: ", min(humidity_to_location))


