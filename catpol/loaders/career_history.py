from scrapy.loader import ItemLoader
import scrapy.loader.processors as processors

import catpol.helpers as helpers


class CareerHistoryLoader(ItemLoader):
    default_output_processor = processors.TakeFirst()
    politician_name = processors.MapCompose(helpers.rws, helpers.beautify_romanian)
    political_party_name = processors.MapCompose(helpers.rws, helpers.beautify_romanian)
