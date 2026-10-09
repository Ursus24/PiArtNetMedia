#Imports from Libraries:
import json
from typing import List, Tuple
from pathlib import Path
import psutil

#Imports from other files:
from artnet import receive_dmx
from output import *

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

def get_paths(target_folder_name: str) -> List[str]:
    usb_mount_point = None
    for partition in psutil.disk_partitions(all=True):
        if (
            'removable' in partition.opts.lower()
            or 'cdrom' in partition.opts.lower()
            or '/Volumes/' in partition.mountpoint
            or partition.mountpoint.startswith(('/media/', '/run/media/'))
        ):
            if partition.mountpoint != '/':
                usb_mount_point = partition.mountpoint
                break

    if not usb_mount_point:
        print('No USB drive detected.')
        return []

    print(f'USB drive found at: {usb_mount_point}')

    # Construct path to the target folder on the USB drive
    target_path = Path(usb_mount_point) / target_folder_name

    if not target_path.exists() or not target_path.is_dir():
        print(f"Folder '{target_folder_name}' not found on the USB drive.")
        return []

    # Recursively collect all file paths inside the folder
    file_paths = [str(file) for file in target_path.rglob('*') if file.is_file()]
    return file_paths


def main():
    engine = PiMediaEngine()
    paths_pictures = get_paths('Pictures')
    paths_videos = get_paths('Videos')

    for values in receive_dmx(start_dmx_channel, artnet_universe, artnet_bind_ip):
        if 0 <= values[0] <= 17:
            engine.show("", values[0], values[2])

        elif 18 <= values[1] <= 33:
            engine.show(paths_pictures[0], values[0], values[2])

        elif 34 <= values[1] <= 49:
            engine.show(paths_pictures[1], values[0], values[2])

        elif 50 <= values[1] <= 65:
            engine.show(paths_pictures[3], values[0], values[2])

        elif 66 <= values[1] <= 81:
            engine.show(paths_pictures[4], values[0], values[2])

        elif 82 <= values[1] <= 97:
            engine.show(paths_pictures[5], values[0], values[2])

        elif 98 <= values[1] <= 113:
            engine.show(paths_pictures[6], values[0], values[2])

        elif 114 <= values[1] <= 128:
            engine.show(paths_pictures[7], values[0], values[2])

        elif 129 <= values[1] <= 144:
            engine.show(paths_pictures[8], values[0], values[2])

        elif 145 <= values[1] <= 160:
            engine.show(paths_pictures[9], values[0], values[2])

        elif 161 <= values[1] <= 176:
            engine.show(paths_pictures[10], values[0], values[2])

        elif 177 <= values[1] <= 192:
            engine.show(paths_pictures[11], values[0], values[2])

        elif 193 <= values[1] <= 208:
            engine.show(paths_pictures[12], values[0], values[2])

        elif 209 <= values[1] <= 224:
            engine.show(paths_pictures[13], values[0], values[2])

        elif 225 <= values[1] <= 240:
            engine.show(paths_pictures[14], values[0], values[2])

        elif 241 <= values[1] <= 255:
            engine.show(paths_pictures[15], values[0], values[2])

        else:
            print(f"Value {values[1]} is out of bounds (must be between 1 and 255).")

main()