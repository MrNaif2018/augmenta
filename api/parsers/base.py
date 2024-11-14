from abc import ABC, abstractmethod


class BaseParser(ABC):
    supported_domains = []

    @abstractmethod
    def parse(self, data):
        pass
