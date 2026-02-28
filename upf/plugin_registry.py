from upf.plugins.sources.file_replay import FileReplaySource
from upf.plugins.sources.health_source import HealthSource

from upf.plugins.processors.temporal_aggregator import TemporalAggregatorProcessor
from upf.plugins.processors.correlation_processor import CorrelationProcessor
from upf.plugins.processors.scoring_processor import ScoringProcessor
from upf.plugins.processors.fusion_gate_processor import FusionGateProcessor
from upf.plugins.processors.metrics_processor import MetricsProcessor

from upf.plugins.sinks.console_sink import ConsoleSink
from upf.plugins.sinks.alert_sink import AlertOnlySink
from upf.plugins.sinks.correlated_sink import CorrelatedAlertSink
from upf.plugins.sinks.scored_sink import ScoredAlertSink

PLUGIN_REGISTRY = {
    #Sources
    "FileReplaySource": FileReplaySource,
    "HealthSource": HealthSource,

    #Processors
    "TemporalAggregatorProcessor": TemporalAggregatorProcessor,
    "CorrelationProcessor": CorrelationProcessor,
    "ScoringProcessor": ScoringProcessor,
    "FusionGateProcessor": FusionGateProcessor,
    "MetricsProcessor": MetricsProcessor,

    #Sinks
    "ConsoleSink": ConsoleSink,
    "AlertOnlySink": AlertOnlySink,
    "CorrelatedAlertSink": CorrelatedAlertSink,
    "ScoredAlertSink": ScoredAlertSink,
}
