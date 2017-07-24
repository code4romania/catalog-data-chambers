import scrapy
import logging

import sys
from scrapy.http import Response

import catpol.loaders as loaders
import catpol.items as items
import catpol.http as http
import string
import catpol.cmdinput as cmdinput
from typing import Sequence, TypeVar, Coroutine


class CdepCareerHistory(scrapy.Spider):
    name = 'cdep_career_history'

    def __init__(self, after=None, years=None):
        super().__init__(after=None, years=None)
        self.years = cmdinput.expand_years(after, years)

    def start_requests(self) -> Coroutine:
        for page in list(self.revert_pagination(self.years)):
            yield http.Reqo(url=page, callback=self.get_politician_urls)

    def revert_pagination(self, years: list) -> list:
        return ['http://www.cdep.ro/pls/parlam/structura2015.de?leg={}&par=A{}'.format(year, char)
                for year in years
                for char in string.ascii_uppercase]

    def get_politician_urls(self, response: Response) -> Coroutine:
        for a in response.css('table a'):
            url = response.urljoin(a.xpath('.//@href').extract_first())
            yield http.Reqo(url=url, callback=self.get_politician_infos)

    # TODO: improve the filter since there are some nulls in the results for some politicians

    def get_politician_infos(self, response: Response) -> Coroutine:
        politician_name = response.xpath('.//*[@id="olddiv"]//*//*[@class="boxTitle"]//h1//text()').extract_first()
        political_party_name = response.xpath('//*[@id="olddiv"]/div/div[3]/h3//text()').extract_first()
        yield items.CareerHistoryItem(politician_name=politician_name, url=response.url,
                                      political_party_name=political_party_name)

