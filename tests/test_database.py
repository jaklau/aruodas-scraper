import unittest
from aruodas_package import DataBase
import sqlalchemy as db
import pandas as pd


# test DataBase class
class TestDataBase(unittest.TestCase):
    database = None

    @classmethod
    def setUpClass(cls):

        # initialise testing database
        cls.database = DataBase("", "", "", "")

        # run database on local sqlite database
        cls.database.engine = db.create_engine(f"sqlite:///docs/tests/aruodas.db")

        # delete all tables in local sqlite database for simpler testing
        cls.database.delete_all_tables()

        cls.database.connect()

    # test is_records method when there is no records
    def test_a_is_records_false(self):
        result = self.database.is_records()
        self.assertEqual(result, False)

    # test write method
    def test_b_write(self):
        df = pd.DataFrame(
            data=
            {'loc1': ['Vilnius'], 'date': ['2022-08-25'], 'loc2': ['Užupis'], 'street': ['Polocko g.'],
             'price': [443400.0], 'rooms': [3.0], 'area': [78.6], 'floor': ['4/4'], 'year': [2022],
             'b_type': ['mūrinis'], 'h_type': ['centrinis kolektorinis'], 'status': ['dalinė apdaila']})
        self.database.write(df)

    # test is_records method when there is records
    def test_c_is_records_true(self):
        result = self.database.is_records()
        self.assertEqual(result, True)

    # test read method for flats table
    def test_d_read(self):
        df = self.database.read("flats")
        self.assertEqual(df["price"].values, 443400.0)

    # test read method for log table
    def test_e_read(self):
        df = self.database.read("log")
        self.assertEqual(df["records"].values, 1)

    @classmethod
    def tearDownClass(cls):
        # delete all tables in local sqlite database for simpler testing
        cls.database.delete_all_tables()


if __name__ == '__main__':
    unittest.main()
