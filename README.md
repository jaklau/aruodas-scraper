# aruodas-scraper
```aruodas-scraper``` package consist of two modules: ```bot.py``` and ```database.py```.
\
\
```bot.py``` uses ```selenium``` to open https://m.aruodas.lt/butai/puslapis/
and extracts from selected page all flats for sale information.
\
\
```database.py``` uses ```SQLAlchemy``` to connect ```PostgreSQL``` database, and 
create tables: ```flats``` and ```log```. You can write scraped data from aruodas
web page to table.
\
\
Main module ```main.py``` is an example how to scrape all pages from aruodas, 
write data to ```pandas``` DataFrame and write flats data to ```PostgreSQL``` 
database table.


## Installation
Install requirements
```bash
pip install -r requirements.txt
```
If you want to have an aruodas-scraped package in your system
use the package manager pip to install ```aruodas-bot``` package.
```bash
pip install .
```

## Tests
Run all tests.
```bash
python -m unittest discover -s tests
```
Run single test for ```bot.py```.
It's tested with static html page source.
```bash
python -m unittest tests/test_bot.py
```
Run single test for ```database.py```.
It's tested with SQLite database file.
```bash
python -m unittest tests/test_database.py
```

## Environment variables
Add these environment variables
```
HOST={database host};
DB={database name};
USER={database user name}
PASSWORD={database password};
PATH={path to chrome driver};
```
In directory PATH, for example "C:\Development", you should put your system Chrome driver,
which you can download from: https://chromedriver.chromium.org/downloads

