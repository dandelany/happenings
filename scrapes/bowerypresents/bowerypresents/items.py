# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class BoweryEventItem(Item):
    source = Field()
    source_url = Field()
    schema_version = Field()

    event_id = Field()
    _id = Field()
    image_urls = Field()
    event_url = Field()
    name = Field()
    supporting = Field()
    date_str = Field()
    doors_time = Field()
    start_time = Field()
    start_timestamp = Field()
    location_name = Field()
    location_city = Field()
    age_restriction = Field()
    price_range = Field()
    bio = Field()
    bio_url = Field()
    ticket_url = Field()
    ical_url = Field()
    gcal_url = Field()
