import requests
import os
from dotenv import load_dotenv

load_dotenv()

COOKIE = os.getenv("COOKIE")
url = f'https://adventofcode.com/2023/day/11/input'
response = requests.get(url, headers={"Cookie": f"session={COOKIE}"})
input_data = response.text

print(input_data)
