from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapes.items import BoweryEventItem

class BoweryPresentsSpider(Spider):
    name = "bowerypresents"
    allowed_domains = ["bowerypresents.com"]
    start_urls = [
        "http://www.bowerypresents.com/see-all-shows/"
    ]

    def parse(self, response):
        sel = Selector(response)
        events = sel.css('div.one-event')

        for event in events:
            event_id = event.css('::attr(id)').re(r'event-id-(\d+)')[0]
            yield Request('http://www.bowerypresents.com/event/' + event_id + '/stub/', callback=self.parse_detail)

    def parse_detail(self, response):
        sel = Selector(response)
        item = BoweryEventItem()
        item['source'] = 'bowerypresents'
        item['source_url'] = response.url
        item['schema_version'] = '0.1.0'

        item['event_id'] = sel.css('.richcal-event-detail::attr(class)').re(r'event-id-(\d+)')[0]
        item['_id'] = ('bowery_' + item['event_id'])
        item['image_urls'] = sel.css('.richcal-event-detail>a>img::attr(src)').extract()

        event_info = sel.css('.richcal-event-info')
        item['event_url'] = event_info.css('.richcal-headliners a::attr(href)').extract()
        item['name'] = event_info.css('.richcal-headliners a::text').extract()
        item['supporting'] = event_info.css('.richcal-supports a::text').extract()
        item['date_str'] = event_info.css('.richcal-dates::text').extract()
        item['doors_time'] = event_info.css('.richcal-times>.doors::text').extract()
        item['start_time'] = event_info.css('.richcal-times>.start::text').extract()
        item['start_timestamp'] = event_info.css('.richcal-times>.start>.value-title::attr(title)').extract()
        item['location_name'] = event_info.css('.location::text').extract()
        item['location_city'] = event_info.css('.richcal-city-state::text').re(r',[\w\s]+, ([A-Z][A-Z])')
        item['age_restriction'] = event_info.css('.richcal-age-restriction::text').extract()
        item['price_range'] = event_info.css('.richcal-ticket-price>.richcal-price-range::text').extract()

        item['bio'] = sel.css('.richcal-bio::text').extract()
        item['bio_url'] = sel.css('.richcal-bio>a::attr(href)').extract()
        item['ticket_url'] = sel.css('.richcal-ticket-link>a::attr(href)').extract()
        item['ical_url'] = sel.css('.richcal-ical-sync>a::attr(href)').extract()
        item['gcal_url'] = sel.css('.richcal-gcal-sync>a::attr(href)').extract()

        return item
