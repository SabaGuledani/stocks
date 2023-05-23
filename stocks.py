import sqlite3
import requests
import json
from win10toast import ToastNotifier
from datetime import date
from datetime import timedelta

today = date.today()
date = today - timedelta(days = 1)

ticker = "AAPL"
apikey = 'WI1GOdsaBMaVnImCyZqgHc__H70kDtJ5'
url = f'https://api.polygon.io/v1/open-close/{ticker}/{date}?adjusted=true&apiKey={apikey}'


r = requests.get(url)

print(r)
print(r.headers)

result_json = r.text
res = json.loads(result_json)
res_structured = json.dumps(res, indent=4)
print(res_structured)

with open(f'{ticker}.json', 'w') as file:
    file.write(result_json)
    json.dump(res, file, indent=4)

date = res['from']
high = res['high']
low = res['low']
avg = (high+low)/2


conn = sqlite3.connect('stocks.sqlite')
cur = conn.cursor()
create = f'''CREATE TABLE IF NOT EXISTS {ticker}
(id INTEGER PRIMARY KEY AUTOINCREMENT,
date DATE,
highest_price FLOAT,
lowest_price FLOAT,
average_price FLOAT);'''

cur.execute(create)

insert = f'INSERT INTO {ticker} (date,highest_price,lowest_price,average_price) VALUES (?,?,?,?)'

cur.execute(insert,(date,high,low,avg))
conn.commit()#ბაზაში ვინახავთ კონკრეტული კომპანიის აქციების ყველაზე მაღალ, დაბალ და საშუალო ფასს კონკრეტული დღეების მიხედვით

toaster = ToastNotifier()
toaster.show_toast(ticker,
f"{ticker}-ის აქციის საშუალო ფასია: {avg} ",
duration=5)
