import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv

file = open('./test.csv', 'r', encoding='utf-8')
reader = csv.reader(file)
for row in reader:
    