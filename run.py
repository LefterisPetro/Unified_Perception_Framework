import asyncio
from upf.core.bus import EventBus
from upf.core.runner import Runner
from upf.config_loader import load_config
from upf.plugins.sources.file_replay import FileReplaySource
from upf.plugins.sources.health_source import HealthSource
from upf.plugins.processors.rules_processor import RulesProcessor
from upf.plugins.processors.temporal_aggregator import TemporalAggregatorProcessor 
from upf.plugins.processors.correlation_processor import CorrelationProcessor
from upf.plugins.sinks.console_sink import ConsoleSink
from upf.plugins.sinks.alert_sink import AlertOnlySink
from upf.plugins.sinks.correlated_sink import CorrelatedAlertSink

async def main():
    config = load_config("profiles/demo.yaml")
    
    bus = EventBus()

    file_source = FileReplaySource(config["source"]["file"])
    health_source = HealthSource()

    temporal_processor = TemporalAggregatorProcessor(
        threshold=50,
        window_seconds=3,
        min_count=2
        )
    
    correlation_processor = CorrelationProcessor()

    console_sink = ConsoleSink()
    alert_sink = AlertOnlySink()
    correlated_sink = CorrelatedAlertSink()

    runner = Runner(
        sources=[file_source, health_source],
        processors=[temporal_processor, correlation_processor],
        sinks=[console_sink, alert_sink, correlated_sink],
        bus=bus
    )
    
    await runner.start()

if __name__ == "__main__":
    asyncio.run(main())