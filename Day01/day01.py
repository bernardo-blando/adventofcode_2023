import requests
import os
from dotenv import load_dotenv

load_dotenv()

COOKIE = os.getenv("COOKIE")
url = f'https://adventofcode.com/2023/day/1/input'
response = requests.get(url, headers={"Cookie": f"session={COOKIE}"})
input_data = response.text

numbers =  {'o1ne':"one",
            't2wo':"two",
            'th3ree':"three",
            'fo4ur':"four", 
            'fi5ve':"five", 
            's6ix':'six', 
            'se7ven':"seven", 
            'ei8ght':"eight", 
            'ni9ne':"nine"
            }

for alg, str in numbers.items():
    input_data = input_data.replace(str, alg) 

input_data = ''.join([i for i in input_data if i.isdigit() or i == '\n'])

input_data = input_data.split('\n')

total = 0
for row in input_data:
    if row == '':
        continue
   
    value = row[0] + row[-1]
    total += int(value)

print(f"The answer is: {total}")


