import yaml
from upf.core.profile_models import ProfileConfig

def load_config(path: str) -> ProfileConfig:
    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    return ProfileConfig(**raw)