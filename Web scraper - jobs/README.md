# Job Searching Web Scraper

## General info
Job Searching Web Scraper is console based application for downloading job offers posted on Ogloszenia.Trojmiasto.pl and save it to SQL Database.

## How it works
App downloads job offers from address entered in file 'scrap.py' and saves all offers to SQL database ('jobs.db'). 
It creates database file and table if they weren't created yet.
Default address can be changed in main file, but it have to lead to page with job offers on Ogloszenia.Trojmiasto.pl 
Default URL leads to job offers from architecture and civil engineering industry.

## Technologies
* Python 3.7
Libraries:
* BeautifulSoup
* Requests
* sqlite3