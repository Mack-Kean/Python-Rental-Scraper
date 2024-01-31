#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def date_string_to_obj(string):
    return datetime.strptime(string, '%d/%b/%Y')

# this url has pretty much everything we will need, just have to parse the contents
URL = "https://thecannon.ca/housing/?search=&wanted_forsale=forsale&beds=3&sortby=date&viewmode=table"
page = requests.get(URL)
print(page)
soup = BeautifulSoup(page.content, "html.parser")
#results = soup.find_all('div', class_='search-results housing table')
results = soup.find_all('tr')
#print(str(results[1])[start_index:end_index])

# open config file for SMPT configuration
server = ''
port = -1
email = ''
password = ''

# config file format is strictly enforced.  Email sending will fail if you deviate from it
try:
    with open("config.txt", 'r') as file:
        server = file.readline().strip()
        port = file.readline().strip()
        email = file.readline().strip()
        password = file.readline().strip()
except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")

# open lastdate file and read the last date
last_date_string = ''
try:
    with open("lastdate.txt", 'r') as file:
        last_date_string = file.readline().strip()
except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
except Exception as e:
    print(f"An error occurred: {e}")

last_date_obj = date_string_to_obj(last_date_string)
print(last_date_obj)

num_recent_listings = 0
recent_listings = []
# start at 1 to skip table header
for i in range(1, len(results)):
    start_index = str(results[i]).find("<!--") + 9 #9 spaces of junk we don't want, found this manually
    end_index = str(results[i]).find("-->") - 6 #6 spaces of junk we don't want

    date_obj = date_string_to_obj(str(results[i])[start_index:end_index])
    
    if date_obj < last_date_obj:
        print(f'{i} recent listings identified')
        num_recent_listings = i
        break

    recent_listings.append(results[i])


email_text = f"{datetime.now()}\n\n"
+ f"Cannon Scraper Update: {num_recent_listings} new listings found since {last_date_string}\n\n"
+ "LISTINGS:\n"

# this loop is where the magic happens
for listing in recent_listings:
    data_elements = listing.find_all('td')
    # for i in range(0,len(data_elements)):
    url = data_elements[0].find_all('a')[0]['href']
    price = data_elements[1].text
    available_from = data_elements[5]

        
#refined_results = results.find_all('tr')