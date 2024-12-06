from langchain_community.document_loaders import WebBaseLoader

from api.parsers.base import BaseParser


class GenericParser(BaseParser):
    def parse(self, data):
        try:
            results = WebBaseLoader([data]).load()
            return results[0] if results else None
        except Exception:
            return None
