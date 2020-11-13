# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from requests import get
from math import floor
import urllib
import xlrd
from datetime import datetime
import matplotlib.pyplot as plt 
from os import remove

URL = 'https://www.nbp.pl/home.aspx?f=/kursy/kursya.html'

page = BeautifulSoup(get(URL).content, 'html.parser')
date = page.find('p', class_='nag').get_text().split(' ')[-1]
print(f'Średnie kursy walut z dnia {date} wg Narodowego Banku Polskiego\n')

currencies = []
table = page.find('table', class_='pad5')
rows = table.find_all('tr')
for row in rows[1:]:
    curr_name = row.find('td', class_='left').get_text()[1:-1]
    curr = row.find_all('td', class_='right')
    curr_code = curr[0].get_text().split(' ')[1]
    curr_rate = float(curr[1].get_text().replace(',','.'))/float(curr[0].get_text().split(' ')[0])
    currencies.append((curr_name, curr_code, curr_rate))

for count, currency in enumerate(currencies, 1):
    print(f'{count}. {currency[0]} ({currency[1]})')
curr_choice = int(input('Wprowadź numer waluty: '))
while curr_choice < 1 or curr_choice > 35:
    curr_choice = int(input('BŁĄD! Wprowadź poprawny numer waluty: '))
name, code, rate = currencies[curr_choice - 1]
print(f'\nWybrana waluta: {name}\n')

print('Dostępne opcje:\n1. Konwersja walut\n2. Ostatnie notowania')
action_choice = int(input('Wprowadź numer opcji: '))
while action_choice < 1 or action_choice > 2:
    action_choice = int(input('\nBŁĄD! Wprowadź numer opcji: '))
    
if action_choice == 1:
    print('\nWybrano konwersję walut')
    print(f'\n1. PLN -> {code}\n2. {code} -> PLN')
    conv_choice = int(input('Jaki typ konwersji? '))
    while conv_choice < 1 or conv_choice > 2:
        conv_choice = int(input("BŁĄD! Jaki typ konwersji? "))
    if conv_choice == 1:
        rate = 1/rate
        code1 = 'PLN'
        code2 = code
    else:
        code1 = code
        code2 = 'PLN'
    print(f'Wybrano {code1} -> {code2}')
    amount = float(input(f'Podaj ilosć {code1}: ').replace(',','.'))
    amount = floor(amount*100)/100
    print(f'{amount:.2f} {code1} = {floor(amount*rate*100)/100:.2f} {code2}')
else:
    print('\nWybrano wykres ostatnich notowań')
    year = datetime.now().year
    archiveURL = f'https://www.nbp.pl/kursy/Archiwum/archiwum_tab_a_{year}.xls'
    urllib.request.urlretrieve(archiveURL, 'archive.xls')
    wb = xlrd.open_workbook('archive.xls')
    sheet = wb.sheet_by_index(0)
    dates = []
    rates = []
    for i in range(sheet.nrows-24, sheet.nrows-4):
        tuple_date = xlrd.xldate_as_tuple(sheet.cell_value(i, 0), wb.datemode)
        temp_date = f'{tuple_date[0]}-{tuple_date[1]}-'
        if tuple_date[2] < 10:
            temp_date += '0' + str(tuple_date[2])
        else:
            temp_date += str(tuple_date[2])
        dates.append(temp_date)
        rates.append(sheet.cell_value(i,curr_choice))
    plt.plot(dates, rates, color='black', marker='o', linestyle='solid')
    plt.xticks(rotation='45')
    plt.xlabel('Data')
    plt.ylabel('Cena waluty [PLN]')
    plt.title(f'''{sheet.cell_value(sheet.nrows-1, curr_choice):.0f}{code} -> PLN
              (ostatnie 20 notowań)''')
    plt.show()
    remove('archive.xls')