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


class NycGovEventItem(Item):
    source = Field()
    source_url = Field()
    schema_version = Field()

    event_guid = Field()
    event_id = Field()
    _id = Field()

    start_timestamp = Field()
    end_timestamp = Field()
    date_str = Field()
    time_str = Field()
    is_canceled = Field()
    nycgov_url = Field()
    is_all_day = Field()
    name = Field()
    description = Field()
    description_short = Field()
    info_email = Field()
    event_url = Field()
    contact_name = Field()
    contact_phone = Field()
    location_name = Field()
    location_address_type = Field()
    location_address = Field()
    location_city = Field()
    location_state = Field()
    location_zip = Field()
    location_boroughs = Field()
    location_map_type = Field()
    location_geometry = Field()

