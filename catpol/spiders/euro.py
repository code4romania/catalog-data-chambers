import json

import scrapy
import xmltodict

import catpol.loaders as loaders
import catpol.items as items
import catpol.http as http


class EuroSpider(scrapy.Spider):

    """www.europarl.europa.eu

    ITEMS CRAWLED:
    - personal_data: birthdate, name, url
    """

    name = 'euro'

    BASE_URL = 'http://www.europarl.europa.eu/meps/en/'
    BASE_IMAGE_URL = 'http://www.europarl.europa.eu/mepphoto/'

    def start_requests(self):
        url = 'http://www.europarl.europa.eu/meps/en/full-list/xml'
        yield http.Reqo(url=url, callback=self.parse_xml)

    def parse_xml(self, response):
        xml_dict = xmltodict.parse(response.body)

        romania = [person for person in xml_dict['meps']['mep']
                   if person['country'] == 'Romania']

        for dude in romania:
            url = self.BASE_URL + dude['id']
            req = http.Reqo(url=url, callback=self.parse_detail)
            req.meta['party'] = dude['nationalPoliticalGroup']
            req.meta['euroGroup'] = dude['politicalGroup']
            req.meta['picture'] = self.BASE_IMAGE_URL + dude['id'] + '.jpg'
            yield req

    def parse_detail(self, response):
        personal_data_loader = loaders.PersonalDataLoader(items.PersonalDataItem())

        personal_data_loader.add_value('party', response.meta['party'])
        personal_data_loader.add_value('eurogroup', response.meta['euroGroup'])
        personal_data_loader.add_value('picture', response.meta['picture'])

        personal_data_loader.add_value('name', response.css('.ep_name.erpl-member-card-full-member-name::text').get())
        personal_data_loader.add_value('birthdate', response.css('#birthDate::text').get())
        personal_data_loader.add_value('birthplace', response.css('#birthPlace::text').get())

        personal_data_loader.add_value('url', response.url)

        yield personal_data_loader.load_item()
