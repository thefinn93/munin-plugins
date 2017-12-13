#!/usr/bin/env python3
import sys
import os
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings()  # Newer firmware uses https with an untrusted cert

config = False
if len(sys.argv) > 1:
    if sys.argv[1] == "config":
        config = True

url = os.environ.get("URL", "https://192.168.100.1/Docsis_system.asp")
status = requests.get(url, verify=False)
soup = BeautifulSoup(status.content, "html.parser")
tds = soup.find_all(attrs={"headers": "ch_pwr"}) + soup.find_all(attrs={"headers": "up_pwr"})

if config:
    model = soup.find(attrs={"headers": "Model"}).text.strip()
    print("\n".join([
        "graph_title {model} Stats",
        "graph_info This graph shows the power levels of a {model} DOCSIS modem",
        "graph_category network",
        "graph_vlabel dBmV"]).format(model=model))

for td in tds:
    key = td.attrs['headers'][0].strip()
    channel = key.split('_')[-1] # "channel_1" or "up_channel_1"
    up = key.startswith("up_")
    name = "{}Channel {}".format("Upstream " if up else "", channel)
    value = td.next.strip()
    if config:
        print("{}.label {}".format(key, name))
    else:
        print("{} {}".format(key, value))
