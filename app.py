from http import client
from bs4 import BeautifulSoup
import requests
import datetime
import os

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# from dotenv import load_dotenv

# load_dotenv()

token = os.environ.get("TOKEN")
org = os.environ.get("ORG")
bucket = os.environ.get("BUCKET")
url = os.environ.get("URL")


def connect_to_influxdb():
    client = InfluxDBClient(url=url, token=token)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    return client, write_api

def get_data(client, write_api):
    url = "https://elen.nu/timpriser-pa-el-for-elomrade-se3-stockholm/"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")

    tables = soup.find_all('table')
    table = soup.find('table', class_="w-full px-4")

    format = "%Y-%m-%d %H:%M"

    for row in table.tbody.find_all('tr'):
    #print(row)

        columns = row.find_all('td')
        #print(columns)

        if(columns != []):
            dt_string = columns[0].text.strip()
            rawprice = columns[1].text.strip()
            price = float(rawprice.split()[0].replace(',', '.'))

            dt_object = datetime.datetime.strptime(dt_string, format)

            point = Point("SpotPrice")\
                .tag("Region", "se3")\
                .field("price", price)\
                .time(dt_object, WritePrecision.S)

            write_api.write(bucket, org, point)


if __name__=="__main__":
    client, write_api = connect_to_influxdb()
    get_data(client, write_api)
    print("Done!")