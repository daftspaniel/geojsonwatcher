import sqlite3
import os.path

from geojsonwatcher.data_structures.feature import Feature
from geojsonwatcher.common.log import log


class FeatureStore:
    def __init__(self, filename):
        self.connection = None
        self.filename = filename
        self.is_new_database = not os.path.isfile(self.filename)
        if self.is_new_database:
            self.create()

    def connect(self):
        log(self.filename)
        self.connection = sqlite3.connect(self.filename)

    def disconnect(self):
        self.connection.close()

    def create(self):
        self.connect()
        self.create_tables()
        self.disconnect()

    def create_tables(self):
        self.connection.execute('''CREATE TABLE FEATURES
                       (ID               INTEGER PRIMARY KEY     NOT NULL,
                        MAG              REAL     NOT NULL,
                        TIME             TEXT     NOT NULL,
                        LOCATION         TEXT     NOT NULL,
                        AREA             TEXT     NOT NULL,
                        URL             TEXT     NOT NULL
                       );''')

    def store_feature(self, feature: Feature):
        self.connection.execute(f"""
                      INSERT INTO FEATURES (MAG,TIME,LOCATION,AREA,URL)
                      VALUES ({feature.mag},'{feature.time}','{feature.site}','{feature.area}','{feature.url}')
                    """)

    def get_record_count(self):
        """ Returns the number of features currently in the database."""
        record = self.connection.execute("""
        SELECT count(*) FROM FEATURES
        """).fetchall()
        return record[0][0]