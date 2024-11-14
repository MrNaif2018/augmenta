import json

from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

from api.parsers.base import BaseParser

api_wrapper_lite = DuckDuckGoSearchAPIWrapper(backend="lite", region="en-us", time=None)
api_wrapper_full = DuckDuckGoSearchAPIWrapper(backend="html", region="en-us", time=None)

duckduckgo = DuckDuckGoSearchResults(output_format="json", num_results=10, api_wrapper=api_wrapper_full)
crunchbase_searcher = DuckDuckGoSearchResults(output_format="json", num_results=10, api_wrapper=api_wrapper_lite)


class DuckDuckGoParser(BaseParser):
    supported_domains = ["duckduckgo.com"]

    def parse(self, name):
        crunchbase_search = json.loads(crunchbase_searcher.invoke(name + " site:crunchbase.com"))
        crunchbase_org = None
        for result in crunchbase_search:
            if "crunchbase.com/organization/" in result["link"]:
                crunchbase_org = result["link"].split("/organization/")[1].split("/")[0]
                break
        return {"crunchbase_org": crunchbase_org, "company": json.loads(duckduckgo.invoke(name))}
