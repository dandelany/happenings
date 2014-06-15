from scrapy.spider import Spider
from scrapy.http import Request
from scrapes.items import NycGovEventItem
import json

class NycGovSpider(Spider):
    name = "nycgov"
    allowed_domains = ["nyc.gov"]
    start_urls = [
        "http://www1.nyc.gov/calendar/api/json/search.htm??&sort=DATE&pageNumber=1"
    ]

    def parse(self, response):
        #parse the first page to figure out pagination
        page = json.loads(unicode(response.body, "ISO-8859-1"))
        num_pages = page['pagination']['numPages']

        for i in range(1, num_pages+1):
            yield Request('http://www1.nyc.gov/calendar/api/json/search.htm??&sort=DATE&pageNumber=' + str(i),
                          callback=self.parse_page)

    def parse_page(self, response):
        page = json.loads(unicode(response.body, "ISO-8859-1"))
        page_items = page['items']
        items = []
        for page_item in page_items:
            item = NycGovEventItem()

            item['source'] = 'nycgov'
            item['source_url'] = response.url
            item['schema_version'] = '0.1.1'

            item['event_id'] = str(page_item['id'])
            item['event_guid'] = page_item['guid']
            item['_id'] = ('nycgov_' + page_item['guid'] + '-' + page_item['startDate'])

            item['start_timestamp'] = page_item['startDate'] if 'startDate' in page_item else None
            item['end_timestamp'] = page_item['endDate'] if 'endDate' in page_item else None
            item['date_str'] = page_item['datePart'] if 'datePart' in page_item else None
            item['time_str'] = page_item['timePart'] if 'timePart' in page_item else None
            item['is_canceled'] = page_item['canceled'] if 'canceled' in page_item else None
            item['nycgov_url'] = page_item['permalink'] if 'permalink' in page_item else None
            item['is_all_day'] = page_item['allDay'] if 'allDay' in page_item else None
            item['name'] = page_item['name'] if 'name' in page_item else None
            item['description'] = page_item['desc'] if 'desc' in page_item else None
            item['description_short'] = page_item['shortDesc'] if 'shortDesc' in page_item else None
            item['info_email'] = page_item['email'] if 'email' in page_item else None
            item['event_url'] = page_item['website'] if 'website' in page_item else None
            item['contact_name'] = page_item['contactName'] if 'contactName' in page_item else None
            item['contact_phone'] = page_item['phone'] if 'phone' in page_item else None
            item['location_name'] = page_item['location'] if 'location' in page_item else None
            item['location_address_type'] = page_item['addressType'] if 'addressType' in page_item else None
            item['location_address'] = page_item['address'] if 'address' in page_item else None
            item['location_city'] = page_item['city'] if 'city' in page_item else None
            item['location_state'] = page_item['state'] if 'state' in page_item else None
            item['location_zip'] = page_item['zip'] if 'zip' in page_item else None
            item['location_boroughs'] = list(page_item['boroughs']) if 'boroughs' in page_item else None
            item['location_map_type'] = page_item['mapType'] if 'mapType' in page_item else None
            item['location_geometry'] = list(page_item['geometry']) if 'geometry' in page_item else None

            items.append(item)
        return items
