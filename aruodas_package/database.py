import sqlalchemy as db
from sqlalchemy.orm import declarative_base
import pandas as pd

# class contains a MetaData object where newly defined Table objects are collected
Base = declarative_base()


# database table class with columns
class Flat(Base):
    __tablename__ = "flats"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    loc1 = db.Column(db.String(100))
    loc2 = db.Column(db.String(100))
    street = db.Column(db.String(100))
    price = db.Column(db.Float)
    rooms = db.Column(db.Float)
    area = db.Column(db.Float)
    floor = db.Column(db.String(10))
    year = db.Column(db.Integer)
    b_type = db.Column(db.String(150))
    h_type = db.Column(db.String(150))
    status = db.Column(db.String(100))


# sql database class for reading, writing data between pandas dataframes and sql database
class DataBase:
    def __init__(self, user, password, host, database):
        # create database engine and connect
        self.engine = db.create_engine(f"postgresql://{user}:{password}@{host}/{database}")
        self.engine.connect()

        # if there is no table in database, create one
        Base.metadata.create_all(self.engine)

    # get all table names
    def table_names(self):
        inspector = db.inspect(self.engine)
        return inspector.get_table_names()

    # read from database and write data to pandas dataframe
    def read(self, table):
        df = pd.read_sql(table, con=self.engine, index_col="id")
        return df

    # write pandas dataframe to database
    def write(self, df: pd.DataFrame, table, if_exists="append"):
        df.to_sql(name=table, con=self.engine, index=False, if_exists=if_exists)
