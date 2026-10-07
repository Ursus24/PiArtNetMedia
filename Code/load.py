import json
from pathlib import Path
from typing import Tuple


def load_config() -> Tuple[int, int, str]:
    json_path = Path(__file__).resolve().parent / "config.json"
    with json_path.open("r", encoding="utf-8") as f:
        config = json.load(f)
    return (
        config["start_dmx_channel"],
        config["artnet_universe"],
        config["artnet_bind_ip"],
    )