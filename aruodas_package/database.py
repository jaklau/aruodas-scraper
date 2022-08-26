import sqlalchemy as db
from sqlalchemy.orm import declarative_base, Session
import pandas as pd
import datetime as dt

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


# database table class with columns
class Log(Base):
    __tablename__ = "log"
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    records = db.Column(db.Integer)


# sql database class for reading, writing data between pandas dataframes and sql database
class DataBase:
    def __init__(self, user, password, host, database):
        # create database engine and connect
        self.engine = db.create_engine("sqlite:///tests/aruodas.db")
        self.session = None

    def connect(self):
        self.engine.connect()

        # if there is no tables in database, then create
        Base.metadata.create_all(self.engine)

        # create session
        self.session = Session(self.engine)

    def delete_all_tables(self):
        Base.metadata.drop_all(self.engine)

    # check if there are already records on current day
    def is_records(self):
        date_now = dt.datetime.now().strftime("%Y-%m-%d")
        record = self.session.query(Log).filter(Log.datetime.between(
            f'{date_now} 00:00:00', f'{date_now} 23:59:59')).first()

        self.session.commit()

        if record is None:
            return False
        else:
            return True

    # write pandas dataframe to database
    def write(self, df: pd.DataFrame, if_exists="append"):
        df.to_sql(name="flats", con=self.engine, index=False, if_exists=if_exists)
        date_time = dt.datetime.now()
        records = int(df["date"].count())
        log = Log(datetime=date_time, records=records)

        self.session.add(log)
        self.session.commit()

    # read from database and write data to pandas dataframe
    def read(self, table):
        df = pd.read_sql(table, con=self.engine, index_col="id")
        return df

