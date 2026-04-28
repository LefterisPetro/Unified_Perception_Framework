from upf.plugins.sources.file_replay import FileReplaySource
from upf.plugins.sources.health_source import HealthSource
from upf.plugins.sources.detection_replay import DetectionReplaySource
from upf.plugins.sources.rf_cue_replay import RFCueReplaySource
from upf.plugins.sources.thermal_cue_replay import ThermalCueReplaySource
from upf.plugins.sources.tick_source import TickSource

from upf.plugins.processors.temporal_aggregator import TemporalAggregatorProcessor
from upf.plugins.processors.correlation_processor import CorrelationProcessor
from upf.plugins.processors.scoring_processor import ScoringProcessor
from upf.plugins.processors.fusion_gate_processor import FusionGateProcessor
from upf.plugins.processors.metrics_processor import MetricsProcessor
from upf.plugins.processors.vision_temporal_processor import VisionTemporalProcessor
from upf.plugins.processors.rule_based_scoring_processor import RuleBasedScoringProcessor
from upf.plugins.processors.rf_fusion_processor import RFFusionProcessor
from upf.plugins.processors.thermal_cue_adapter import ThermalCueAdapter
from upf.plugins.processors.vision_cue_adapter import VisionCueAdapter
from upf.plugins.processors.rf_cue_adapter import RFCueAdapter
from upf.plugins.processors.incident_manager import IncidentManagerProcessor

from upf.plugins.sinks.console_sink import ConsoleSink
from upf.plugins.sinks.alert_sink import AlertOnlySink
from upf.plugins.sinks.correlated_sink import CorrelatedAlertSink
from upf.plugins.sinks.scored_sink import ScoredAlertSink
from upf.plugins.sinks.detection_sink import DetectionSink
from upf.plugins.sinks.rf_sink import RFCueSink
from upf.plugins.sinks.incident_sink import IncidentSink
from upf.plugins.sinks.incident_log_sink import IncidentLogSink

PLUGIN_REGISTRY = {
    #Sources
    "FileReplaySource": FileReplaySource,
    "HealthSource": HealthSource,
    "DetectionReplaySource": DetectionReplaySource,
    "RFCueReplaySource": RFCueReplaySource,
    "ThermalCueReplaySource": ThermalCueReplaySource,
    "TickSource": TickSource,
    
    #Processors
    "TemporalAggregatorProcessor": TemporalAggregatorProcessor,
    "CorrelationProcessor": CorrelationProcessor,
    "ScoringProcessor": ScoringProcessor,
    "FusionGateProcessor": FusionGateProcessor,
    "MetricsProcessor": MetricsProcessor,
    "VisionTemporalProcessor": VisionTemporalProcessor,
    "RuleBasedScoringProcessor": RuleBasedScoringProcessor,
    "RFFusionProcessor": RFFusionProcessor,
    "ThermalCueAdapter": ThermalCueAdapter,
    "VisionCueAdapter": VisionCueAdapter,
    "RFCueAdapter": RFCueAdapter,
    "IncidentManagerProcessor": IncidentManagerProcessor,


    #Sinks
    "ConsoleSink": ConsoleSink,
    "AlertOnlySink": AlertOnlySink,
    "CorrelatedAlertSink": CorrelatedAlertSink,
    "ScoredAlertSink": ScoredAlertSink,
    "DetectionSink": DetectionSink,
    "RFCueSink": RFCueSink,
    "IncidentSink": IncidentSink,
    "IncidentLogSink": IncidentLogSink
}
