from selenium import webdriver
from bs4 import BeautifulSoup


URL = "https://m.aruodas.lt/butai/puslapis/"

STREETS = ["g.", "skg.", "aklg.", "al.", "pr.", "a.", "skv.", "tak.", "pl.", "kel.",
           "kl.", "aplinkl.", "vieškl.", "krant."]

B_TYPES = ["mūrinis", "blokinis", "monolitinis", "medinis", "karkasinis", "rąstinis"]
H_TYPES = ["centrinis", "centrinis kolektorinis", "dujinis", "elektra", "geoterminis",
           "aeroterminis", "kietu kuru", "skystu kuru", "saulės energija"]
STATUSES = ["įrengtas", "dalinė apdaila", "neįrengtas", "nebaigtas statyti", "pamatai"]


class AruodasBot:
    # aruodas has bot detecting functions so use selenium to start web browser and extract page source
    # create beautiful soup for that source
    # this method with bs is way faster than crawl all parameters with selenium
    def __init__(self, driver: webdriver, page=1):
        self.page = page
        self.data = list()
        self.driver = driver
        self.webpage = f"{URL}{page}"
        self.soup = None

    def get(self):
        # open web page with browser
        self.driver.get(self.webpage)

        # extract page source
        page_source = self.driver.page_source

        # create beautiful soup for page source
        self.soup = BeautifulSoup(page_source, 'lxml')

    # on aruodas page find last page number. For example: if there is pages: 1,2,3...280 method returns 280.
    def find_last_page(self):
        page = self.soup.find("div", class_="page-select-v2").find("a").get_text(strip=True).split(" iš ")[1]
        return int(page)

    # crawl aruodas page and parse needed data
    def read(self):
        # find all rows with flat information
        rows = self.soup.find_all("li", class_="result-item-v3")
        # go through each flat to extract needed data
        for i in rows:
            # try to avoid advertise, because ads has same class name as flat rows
            try:
                item = dict()

                # parse location data
                location = i.find("span", class_="item-address-v3").get_text(strip=True).split(", ")
                # 1st item of location description goes to loc1
                item["loc1"] = location[0]
                item["loc2"] = None
                item["street"] = None
                loc_len = len(location)
                # if there is total 2 items in location description, we have to find out if 2nd item is a street
                if loc_len == 2:
                    item["loc2"] = location[1]
                    for x in STREETS:
                        if x in location[1]:
                            item["loc2"] = None
                            item["street"] = location[1]
                            break
                # if there is total 3 items in location description, 2nd item goes to loc2, 3rd element goes to street
                elif loc_len == 3:
                    item["loc2"] = location[1]
                    item["street"] = location[2]

                # parse: price, number of rooms, area(m2), floor, year, building type, heating type and status
                description = i.find("span", class_="item-description-v3").get_text(strip=True).split(", ")
                price = i.find("span", class_="item-price-main-v3").get_text(strip=True).split("(")
                item["price"] = float(price[0].replace("€", "").replace(" ", ""))
                item["rooms"] = float(description[0].replace(" k.", ""))
                item["area"] = float(description[1].replace(" m²", "").replace(",", "."))
                item["floor"] = description[2].replace(" aukšt.", "")
                item["year"] = int(description[3].replace(" m.", ""))
                other = description[4:]
                # find building type
                for x in B_TYPES:
                    if x in other:
                        item["b_type"] = x
                # find heating type
                for x in H_TYPES:
                    if x in other:
                        if "h_type" not in item:
                            item["h_type"] = x
                        else:
                            item["h_type"] += ", " + x
                # find status
                for x in STATUSES:
                    if x in other:
                        item["status"] = x

                # add flat data to whole page data
                self.data.append(item)
            except AttributeError:
                pass

    # print to terminal parsed data
    def print(self):
        print(f"page: {self.page}, data: {self.data}")
