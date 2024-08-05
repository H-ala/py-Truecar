import re
import requests
import mysql.connector
from bs4 import BeautifulSoup

car = input()
car = car.replace(' ','-')
car = car.lower()

r = requests.get('https://www.truecar.com/used-cars-for-sale/listings/'+ car+ '/')
soup = BeautifulSoup(r.text, 'html.parser')

models_list = [] 
prices_list = [] 
miles_list = []

models = soup.find_all('div', attrs = {'data-test':'vehicleCardTrim'}, limit=20)
for model in models:
    models_list.append(model.text)

prices = soup.find_all('div', attrs = {'data-test':'vehicleCardPricingBlockPrice'}, limit=20)
for price in prices:
    prices_list.append(price.text)

miles = soup.find_all('div', attrs = {'class':'linkable card card-shadow vehicle-card'}, limit=20)
for mile in miles:
    miles_list.append(re.findall(r'(\d+) miles', mile.text))

result = list(zip(models_list, prices_list, miles_list))

cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='truecar')
cursor = cnx.cursor()
for i in result:
    cursor.execute('INSERT INTO cars (model, price, miles) VALUES (%s, %s, %s)', (i[0], i[1], i[2][0]))
cnx.commit()
cnx.close()

