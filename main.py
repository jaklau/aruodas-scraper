import os
from selenium import webdriver
import pandas as pd
from aruodas_scraper import Bot, DataBase

USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
HOST = os.environ["HOST"]
DB = os.environ["DB"]

# connect to database, if table does not exist, create one
db = DataBase(USER, PASSWORD, HOST, DB)
db.connect()

# check in log table if there is any records on current day
if db.is_records():
    print("Records are already on this day")

else:
    # chrome options to not load images
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    # initialize selenium browser driver
    driver = webdriver.Chrome(options=chrome_options)

    # run first page bot
    bot = Bot(driver)
    bot.get()
    bot.read()
    bot.print()

    # first page docs save to main docs
    data = bot.data

    # on web page find number of all pages
    page = bot.find_last_page()

    # crawl all remained pages
    for i in range(2, 4):
        bot = Bot(driver, i)
        bot.get()
        bot.read()
        bot.print()
        data += bot.data

    # quit() command quits the entire browser session with all its tabs and windows
    driver.quit()

    # save docs to pandas dataframe, drop duplicates, add date column
    df = pd.DataFrame(data=data)
    df.drop_duplicates(keep='first', inplace=True, ignore_index=True)

    # write dataframe to database table and write info about record to log table
    db.write(df)
