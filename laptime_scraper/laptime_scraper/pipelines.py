# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import psycopg2


class PostgresLapTimesCleanPipeline:
    """ Cleaning the data scraped from the website
    lap - changing the datatype to int
    laptime - transforming the 00:00:00 format to the number of miliseconds,
    """

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'race':
                value = adapter.get(field_name)
                if adapter[field_name] != None:
                    adapter[field_name] = value.strip()

        # changing the lap to integer
        value = adapter.get('lap')
        adapter['lap'] = int(value)

        #transforming the 00:00:00 format to the number of miliseconds,
        value = adapter.get('lap_time')
        minutes, rest =  value.split(":")
        minutes = int(minutes)
        seconds, milliseconds = map(int, rest.split("."))
        adapter['lap_time'] = minutes * 60 * 1000 + seconds * 1000 + milliseconds 

        return item


class PostgresLapTimesSQLPipeline:
    """ Pipeline dedicated to insterting the clean data to the local postgresql database Laptimes"""

    def __init__(self):
        hostname = 'localhost'
        username = 'postgres'
        password = '*****'
        database = 'Laptimes'

        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

        self.cur.execute("""
                    CREATE TABLE IF NOT EXISTS Laptimes (  
                        LapID SERIAL,
                        LapNumber int NOT NULL DEFAULT 0,
                        RaceName varchar(100) NOT NULL,
                        DriverSurname varchar(50) NOT NULL,
                        DriverName varchar(50) NOT NULL,
                        Position varchar(10), 
                        Laptime int NOT NULL DEFAULT 0
                
                     );""")
    def process_item(self, item, spider):

        self.cur.execute(""" insert into Laptimes (LapNumber, RaceName, DriverSurname, DriverName, Position, Laptime) values (%s,%s,%s,%s,%s,%s)""", (
            item["lap"],
            item["race"],
            item["driver_surname"],
            item['driver_name'],
            item["position"],
            item["lap_time"]
        ))

        
        self.connection.commit()
        return item
        
        def close_spider(self, spider):

            ## Close cursor & connection to database 
            self.cur.close()
            self.connection.close()


