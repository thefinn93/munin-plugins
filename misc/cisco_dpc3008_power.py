#!/usr/bin/env python
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
model = soup.find(attrs={"headers": "Model"}).text.strip()
tables = soup.find_all('table', attrs={'class': 'std'})

graphs = {
    "power_down": {
        "graph": {
            "title": "{model} Downstream Power",
            "info": "Shows the levels on the downstream channels",
            "category": "network",
            "vlabel": "dBmV"
        }, "fields": {}
    },
    "power_up": {
        "graph": {
            "title": "{model} Upstream Power",
            "info": "Shows the levels on the upstream channels",
            "category": "network",
            "vlabel": "dBmV"
        }, "fields": {}
    },
    "snr_down": {
        "graph": {
            "title": "{model} Downstream Signal to Noise Ratio",
            "info": "Shows the SNR on the downstream channels",
            "category": "network",
            "vlabel": "dB"
        }, "fields": {}
    }
}

# Downstream
for tr in tables[3].find_all('tr')[1:]:
    power_td, snr_td = tr.find_all('td')[1:]
    key = power_td.attrs['headers'][0].strip()
    label = "Channel {}".format(key.split("_")[-1])
    power = power_td.next.strip()
    snr = snr_td.next.strip()
    graphs['power_down']['fields'][key] = {
        "label": label,
        "value": power
    }
    graphs['snr_down']['fields'][key] = {
        "label": label,
        "value": snr
    }

# Upstream
for tr in tables[4].find_all('tr')[1:]:
    power_td = tr.find('td', attrs={"headers": "up_pwr"})
    key = power_td.attrs['headers'][0].strip()
    label = "Channel {}".format(key.split("_")[-1])
    power = power_td.next.strip()
    graphs['power_up']['fields'][key] = {
        "label": label,
        "value": power
    }



for graph_name, graph in graphs.items():
    print("multigraph {}_{}".format(os.path.basename(sys.argv[0]), graph_name))
    if config:
        for field, value in graph['graph'].items():
            print("graph_{} {}".format(field, value.format(model=model)))
        for field, value in graph['fields'].items():
            print("{}.label {}".format(field, value['label']))
    else:
        for field, value in graph['fields'].items():
            print("{}.value {}".format(field, value['value']))
