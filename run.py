import asyncio
import argparse
import inspect
from upf.core.bus import EventBus
from upf.core.runner import Runner
from upf.core.exceptions import ProfileValidationError
from upf.config_loader import load_config
from upf.plugin_registry import PLUGIN_REGISTRY

def instantiate_component(component_config):

    if "type" not in component_config:
        raise ProfileValidationError(
            f"Missing 'type' in component config: {component_config}"
        )
    
    component_type = component_config["type"]
    params = component_config.get("params", {})

    if component_type not in PLUGIN_REGISTRY:
        raise ProfileValidationError(
            f"Unknown plugin type '{component_type}'. "
            f"Available: {list(PLUGIN_REGISTRY.keys())}"
        )

    cls = PLUGIN_REGISTRY[component_type]
    
    #Validate constructor parameters
    signature = inspect.signature(cls.__init__)
    valid_params = list(signature.parameters.keys())
    if "self" in valid_params:
        valid_params.remove("self")

    for param in params.keys():
        if param not in valid_params:
            raise ProfileValidationError(
                f"Invalid parameter '{param}' for plugin '{component_type}'. "
                f"Valid params: {valid_params}"
            )
        
    try:
        return cls(**params)
    except TypeError as e:
        raise ProfileValidationError(
            f"Failed to instantiate '{component_type}': {str(e)}"
        )

async def main(profile_path):
    
    config = load_config(profile_path)

    required_sections = ["sources", "processors", "sinks"]
    for section in required_sections:
        if section not in config:
            raise ProfileValidationError(
                f"Profile missing required section: '{section}'"
            )
    
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