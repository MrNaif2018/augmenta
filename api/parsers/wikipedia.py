from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from api.parsers.base import BaseParser

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())


class WikipediaParser(BaseParser):
    supported_domains = ["wikipedia.org"]

    def parse(self, name):
        return wikipedia.invoke(name)
