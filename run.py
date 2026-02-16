import asyncio
import argparse
from upf.core.bus import EventBus
from upf.core.runner import Runner
from upf.config_loader import load_config
from upf.plugin_registry import PLUGIN_REGISTRY

def instantiate_component(component_config):
    component_type = component_config["type"]
    params = component_config.get("params", {})

    cls = PLUGIN_REGISTRY[component_type]
    return cls(**params)

async def main(profile_path):
    
    config = load_config(profile_path)
    
    bus = EventBus()

    sources = [instantiate_component(s) for s in config["sources"]]
    processors = [instantiate_component(p) for p in config["processors"]]
    sinks = [instantiate_component(s) for s in config["sinks"]]

    runner = Runner(
        sources=sources,
        processors=processors,
        sinks=sinks,
        bus=bus
    )
    
    await runner.start()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        default="profiles/demo.yaml",
        help="Path to profile YAML file"
    )

    args = parser.parse_args()

    asyncio.run(main(args.profile))