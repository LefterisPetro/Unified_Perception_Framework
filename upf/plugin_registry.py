from upf.plugins.sources.file_replay import FileReplaySource
from upf.plugins.sources.health_source import HealthSource

from upf.plugins.processors.temporal_aggregator import TemporalAggregatorProcessor
from upf.plugins.processors.correlation_processor import CorrelationProcessor

from upf.plugins.sinks.console_sink import ConsoleSink
from upf.plugins.sinks.alert_sink import AlertOnlySink
from upf.plugins.sinks.correlated_sink import CorrelatedAlertSink


PLUGIN_REGISTRY = {
    #Sources
    "FileReplaySource": FileReplaySource,
    "HealthSource": HealthSource,

    #Processors
    "TemporalAggregatorProcessor": TemporalAggregatorProcessor,
    "CorrelationProcessor": CorrelationProcessor,

    #Sinks
    "ConsoleSink": ConsoleSink,
    "AlertOnlySink": AlertOnlySink,
    "CorrelatedAlertSink": CorrelatedAlertSink,
}
