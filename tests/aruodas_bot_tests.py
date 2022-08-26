import unittest
from selenium import webdriver
from aruodas_package import AruodasBot
import os


# test AruodasBot class
class TestAruodasBot(unittest.TestCase):
    def setUp(self):
        # initialize selenium browser driver
        driver = webdriver.Chrome()

        # run tests page bot
        self.bot = AruodasBot(driver)

        # get current absolute direction
        dirname = os.path.dirname(__file__)
        # get absolute direction to html file
        filename = os.path.join(dirname, "../docs/tests/aruodas.html")
        # open static html file with driver
        self.bot.webpage = f"file:///{filename}"
        self.bot.get()
        self.bot.read()

        driver.quit()

    # test find_last_page method
    def test_find_last_page(self):
        page = self.bot.find_last_page()
        self.assertEqual(page, 279)

    # test read method
    def test_read(self):
        data = self.bot.data
        self.assertEqual(data[1],
                         {'loc1': 'Vilnius', 'loc2': 'Užupis', 'street': 'Polocko g.', 'price': 443400.0,
                          'rooms': 3.0, 'area': 78.6, 'floor': '4/4', 'year': 2022, 'b_type': 'mūrinis',
                          'h_type': 'centrinis kolektorinis', 'status': 'dalinė apdaila'})


if __name__ == '__main__':
    unittest.main()
