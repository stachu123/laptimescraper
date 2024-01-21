import scrapy
from laptime_scraper.items import LaptimeItem


class LaptimesSpider(scrapy.Spider):
    name = "laptimespider"
    allowed_domains = ["pitwall.app"]
    start_urls = ["https://pitwall.app/analysis/race-report"]

    def parse(self, response):
        races_ids = response.css('select[name="race"] option::attr(value)').getall()
        driver_ids = response.css('select[name="driver"] option::attr(value)').getall()

        # for driver in driver_ids:
        #     for race in races_ids:
        #         url = f'https://pitwall.app/analysis/race-report?utf8=%E2%9C%93&season=75&race={race}&driver={driver}&button='
        #         yield scrapy.Request(url, callback=self.parse_race_data)
        url = f'https://pitwall.app/analysis/race-report?utf8=%E2%9C%93&season=75&race=1178&driver=17&button='
        yield scrapy.Request(url, callback=self.parse_race_data)

    def parse_race_data(self, response):
        table = response.css('.data-table.data-table-small > tbody')
        rows = table.css('tr')
        laptimeitem = LaptimeItem()
        for row in rows:
            laptimeitem["lap"] = row.xpath('td//text()')[0].extract()
            laptimeitem["position"] = row.xpath('td//text()')[1].extract()
            laptimeitem["lap_time"] = row.xpath('td//text()')[2].extract()
            # laptimeitem["pit_stop_time"]: row.xpath('td//text()')[3].extract()
            laptimeitem["race"] = response.xpath("//div[@id='race-report'][1]/div[@class='section'][1]/h3[@class='block-title'][1]/text()[1]").get()
            laptimeitem["driver_name"] = response.xpath("//span[@class='minmdlg'][1]/text()[1]").get()
            laptimeitem["driver_surname"] = response.xpath("//div[@id='race-report'][1]/div[@class='section'][1]/h3[@class='block-title'][1]/text()[2]").get()

            yield laptimeitem




