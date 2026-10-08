#Imports from Libraries:
import json
from typing import Tuple
from pathlib import Path

#Imports from other files:
from artnet import receive_dmx
from output import showImage

#Loading the config file:
def load_config() -> Tuple[int, int, str]:
    json_path = Path(__file__).resolve().parent / "config.json"
    with json_path.open("r", encoding="utf-8") as f:
        config = json.load(f)
    return (
        config["start_dmx_channel"],
        config["artnet_universe"],
        config["artnet_bind_ip"],
    )
start_dmx_channel, artnet_universe, artnet_bind_ip = load_config()



def main():
    for values in receive_dmx(start_dmx_channel, artnet_universe, artnet_bind_ip):
        print(values)
        showImage("image.png" if values[1] == 255 else "")

main()