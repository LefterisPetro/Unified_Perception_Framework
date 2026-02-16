import asyncio

class Runner:
    def __init__(self, sources, processors, sinks, bus):
        self.sources = sources
        self.processors = processors
        self.sinks = sinks
        self.bus = bus

    async def start(self):
        for p in self.processors:
            self.bus.register_processor(p)

        for s in self.sinks:
            self.bus.register_sink(s)

        source_tasks = [
            asyncio.create_task(source.start(self.bus))
            for source in self.sources
        ]

        bus_task = asyncio.create_task(self.bus.run())

        await asyncio.gather(*source_tasks, bus_task)
