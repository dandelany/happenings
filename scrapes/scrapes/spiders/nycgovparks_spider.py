from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapes.items.nycgovparks import NycGovParksEventItem
from pprint import pprint as pp

class NycGovParksSpider(Spider):
    name = "nycgovparks"
    allowed_domains = ["nycgovparks.org"]
    start_urls = [
        "http://www.nycgovparks.org/events/p1"
    ]
    base_url = "http://www.nycgovparks.org"

    def absolute_url(self, url):
        if url[0:4] == 'http':
            return url
        elif url[0] == '/':
            return self.base_url + url
        # todo relative urls
        return url

    def link_or_text(self, sel):
        link_text = sel.css('a::text').extract()
        return link_text if len(link_text) > 0 else sel.css('::text').extract()

    def parse(self, response):
        sel = Selector(response)
        first_page = 1
        last_page = 100
        self.i = 1
        for i in range(first_page, last_page+1):
            yield Request(self.base_url + "/events/p" + str(i), callback=self.parse_events_page)

    def parse_events_page(self, response):
        sel = Selector(response)
        events = sel.css('.event')
        for event in events:
            event_url = event.css('.event-title a::attr(href)').extract()[0]
            event_url = self.absolute_url(event_url)
            yield Request(event_url, callback=self.parse_event)

    def parse_event(self, response):
        print 'parsing event #', str(self.i)

        sel = Selector(response)
        event = sel.css('.single_event')
        item = NycGovParksEventItem()
        item['source'] = 'nycgovparks'
        item['source_url'] = response.url
        item['schema_version'] = '0.1.2'

        item['name'] = event.css('.single_event_head>h1::text').extract()

        cal_links = event.css('.cal_service_links>ul>li>a::attr(href)')
        item['gcal_url'] = self.absolute_url(cal_links.re(r'(^.+google.+$)')[0])
        item['ical_url'] = self.absolute_url(cal_links.re(r'(^.+iCal.+$)')[0])

        item['date_str'] = event.css('.single_event_start_date>strong::text').extract()
        item['start_timestamp'] = event.css('meta[itemprop*=startDate]::attr(content)').extract()
        item['end_timestamp'] = event.css('meta[itemprop*=endDate]::attr(content)').extract()
        item['event_alert'] = event.css('p.alert::text').extract()
        item['description'] = '\n'.join(event.css('div[itemprop=description]>p').extract())

        event_body = sel.css('#single_event_body')
        item['location_lat'] = event_body.css('meta[itemprop=latitude]::attr(content)').extract()
        item['location_lng'] = event_body.css('meta[itemprop=longitude]::attr(content)').extract()
        item['location_address'] = event_body.css('div[itemprop=streetAddress]::text').extract()
        item['location_locality'] = event_body.css('div[itemprop=addressLocality]::text').extract()

        cur_heading = ''
        for el in event_body.css('h3, p, ul'):
            if len(el.css('h3')) > 0:
                cur_heading = ''.join(el.css('h3::text').extract())
            elif cur_heading == 'Cost':
                item['price_range'] = el.css('::text').extract()
            elif cur_heading == 'Event Organizer':
                item['organizer'] = self.link_or_text(el)
                item['organizer_url'] = el.css('a::attr(href)').extract()
            elif cur_heading == 'Contact Number':
                item['contact_phone'] = el.css('::text').extract()
            elif cur_heading == 'Contact Email':
                item['contact_email'] = self.link_or_text(el)
            elif cur_heading == 'Categories':
                item['categories'] = el.css('a::text').extract()

        event_links = event_body.css('#event_links a')
        if(len(event_links) > 0):
            item['event_links'] = []
            for link in event_links:
                item['event_links'].append((link.css('::text').extract(), link.css('::attr(href)').extract()))

        self.i += 1
        return item
