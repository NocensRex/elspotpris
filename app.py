from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
from influxdb import InfluxDBClient
import time

from dotenv import load_dotenv

load_dotenv()

url = "https://elen.nu/timpriser-pa-el-for-elomrade-se3-stockholm/"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")

client = InfluxDBClient(host='localhost', port=8086)

tables = soup.find_all('table')

table = soup.find('table', class_="w-full px-4")

data = {
    'Date': [],
    'Time': [],
    'Price/SEK': []}

for row in table.tbody.find_all('tr'):
    #print(row)

    columns = row.find_all('td')
    #print(columns)

    if(columns != []):
        datetime = columns[0].text.strip()
        date = datetime.split()[0]
        time = datetime.split()[1]
        rawprice = columns[1].text.strip()
        price = float(rawprice.split()[0].replace(',', '.'))

        data['Date'].append(date)
        data['Time'].append(time)
        data['Price/SEK'].append(price)

df = pd.DataFrame.from_dict(data)

df = df.set_index('Date')

df.plot(x='Time', y='Price/SEK')

plt.plot(df['Time'], df['Price/SEK'])
