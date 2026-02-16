from abc import ABC, abstractmethod
from typing import List

class ISource(ABC):
    @abstractmethod
    async def start(self, bus):
        pass

class IProcessor(ABC):
    @property
    @abstractmethod
    def supported_event_types(self) -> List[str]:
        pass

    @abstractmethod
    async def process(self, event, bus):
        pass
    
class ISink(ABC):
    
    @property
    @abstractmethod
    def supported_event_types(self):
        pass

    @abstractmethod
    async def handle(self, event):
        pass
    