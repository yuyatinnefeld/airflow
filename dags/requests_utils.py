import requests
import pandas as pd
import json
import datetime as dt


def request_url():
    response = requests.get('https://api.github.com/events')
    url = response.url
    status = response.status_code
    encoding = response.encoding
    time = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    data = {
        'time':time, 
        'url':url, 
        'status':status, 
        'encoding':encoding
    }
    return data

def save_text():
    data = request_url()
    with open('data/request.txt', 'a') as outfile:
        outfile.write(str(data) + ', \n')

def save_json():
    data = request_url()
    with open('data/request.json', 'a') as outfile:
        json.dump(data, outfile)

def save_csv():
    data = {'time': ['2021-01-27 21:02', '2021-01-27 21:07'], 'url':['https://api.github.com/events', 'https://www.wamo.com']}
    df = pd.DataFrame(data=data)
    df.to_csv (r'data/request.csv', index = False)