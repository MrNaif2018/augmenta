from api.parsers.crunchbase import CrunchbaseParser
from api.parsers.duckduckgo import DuckDuckGoParser
from api.parsers.generic import GenericParser
from api.parsers.wikipedia import WikipediaParser

PARSERS = [GenericParser, CrunchbaseParser, WikipediaParser, DuckDuckGoParser]
domain_map = {domain: parser for parser in PARSERS for domain in parser.supported_domains}


def parse(domain, name):
    parser = domain_map.get(domain)
    if not parser:
        return GenericParser().parse(name)
    return parser().parse(name)
