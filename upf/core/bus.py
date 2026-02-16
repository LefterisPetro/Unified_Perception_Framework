import asyncio

class EventBus:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.processors = []
        self.sinks = []

    async def publish(self, event):
        await self.queue.put(event)
    
    def register_processor(self, processor):
        self.processors.append(processor)

    def register_sink(self, sink):
        self.sinks.append(sink)
    
    async def run(self):
        while True:
            event = await self.queue.get()

            for processor in self.processors:
                if event.event_type in processor.supported_event_types:
                    await processor.process(event, self)

            for sink in self.sinks:
                if event.event_type in sink.supported_event_types:
                    await sink.handle(event)
                