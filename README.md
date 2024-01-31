<h2> F1 Lap Time Scraper and Database Inserter. </h2>

The project was created with python and scrapy to extract Formula 1 lap time data from a designated website. 
The scraped data is then stored in a local PostgreSQL database for further analysis (future projects).
The data is scraped only for the 2023 season.

<h2>Features</h2>

Scrapy Spider: The project includes a Scrapy spider that navigates through the target website, extracts lap time data, and parses it for further processing.

PostgreSQL Database Integration: The scraped lap time data is inserted into a local PostgreSQL database, providing a structured and scalable way to store and manage the information.


<h2>Requirements</h2>
Make sure you have the following installed before running the project:

* Python 3.x
* Scrapy
* PostgreSQL
* Psycopg



<h2> Database Schema </h2>
The scraped lap time data is stored in a PostgreSQL database with the following schema:


``` sql
CREATE TABLE IF NOT EXISTS Laptimes (  
                        LapID SERIAL,
                        LapNumber int NOT NULL DEFAULT 0,
                        RaceName varchar(100) NOT NULL,
                        DriverSurname varchar(50) NOT NULL,
                        DriverName varchar(50) NOT NULL,
                        Position varchar(10), 
                        Laptime int NOT NULL DEFAULT 0);
```

