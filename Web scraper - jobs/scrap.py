# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from requests import get
import sqlite3

URL = 'https://ogloszenia.trojmiasto.pl/praca-zatrudnie/architektura-budownictwo/'

database = sqlite3.connect("jobs.db")
cursor = database.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")


if 'jobs' not in [table[0] for table in cursor.fetchall()]:
    cursor.execute('''CREATE TABLE jobs (job TEXT, link TEXT, company TEXT,
                                         location TEXT);''')
else:
    cursor.execute('DELETE FROM jobs')    

page = get(URL)
bs = BeautifulSoup(page.content, 'html.parser')
last_page = int(bs.find('a', title='ostatnia strona').get('data-page-number'))

for number in range(1,last_page+1):
    URL2 = URL + f'?strona={number}'
    page = get(URL2)
    bs = BeautifulSoup(page.content, 'html.parser')
    print(f'Pracuję nad stroną {number} z {last_page}')
    for offer in bs.find_all('div', class_='list--item--work'):
        temp = offer.find('a', class_='list__item__content__title__name')
        job = temp.get_text()
        link = temp.get('href')
        location = offer.find('p', class_='list__item__content__subtitle').get_text()
        try:
            company = offer.find('p', class_='list__item__details__info').get_text()
        except:
            company = " "
        cursor.execute('INSERT INTO jobs VALUES (?,?,?,?)',(job, link, company, location))
        database.commit()
database.close()