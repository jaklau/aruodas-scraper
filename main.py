from selenium import webdriver
import pandas as pd
import datetime as dt
from aruodas_package import AruodasBot, DataBase, group_by_region

USER = "postgres"
PASSWORD = "123456"
HOST = "localhost"
DB = "aruodas"


# chrome options to not load images
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

# initialize selenium browser driver
driver = webdriver.Chrome(options=chrome_options)

# run first page bot
bot = AruodasBot(driver)
bot.get()
bot.read()
bot.print()

# first page data save to main data
data = bot.data

# on web page find number of all pages
page = bot.find_last_page()

# crawl all remained pages
for i in range(2, 4):
    bot = AruodasBot(driver, i)
    bot.get()
    bot.read()
    bot.print()
    data += bot.data

# quit() command quits the entire browser session with all its tabs and windows
driver.quit()

# get current date as string: 20220101
date = dt.datetime.now().strftime("%Y%m%d")

# save data to pandas dataframe, drop duplicates, add date column
df = pd.DataFrame(data=data)
df.drop_duplicates(keep='first', inplace=True, ignore_index=True)
df.insert(loc=0, column="date", value=date)
df["date"] = pd.to_datetime(df["date"])

# connect to database, if table does not exist, create one
db = DataBase(USER, PASSWORD, HOST, DB)

# write dataframe to database
db.write(df, f"flats")
