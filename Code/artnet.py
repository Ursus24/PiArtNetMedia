#Imports from Libraries:
from threading import Event
from typing import Optional

#Imports from other files:
from python_artnet import Artnet

#Function to receive DMX values from Art-Net:s
def receive_dmx(
    channel: int,   #Starting DMX channel to listen 10 Channels after that are returned
    universe: int,  #Art-Net universe to listen to
    bind_ip: str,   # IP address to bind the Art-Net socket to
    stop_event: Optional[Event] = None,  # Optional threading event to stop the loop
):
    channels = list(range(channel, channel + 10))

    artnet = Artnet(bind_ip)
    last_values = None

    try:
        while stop_event is None or not stop_event.is_set():
            buffer = artnet.readBuffer()

            if buffer is not None and 0 <= universe < len(buffer):
                packet = buffer[universe]
                if packet.data is not None:
                    values = [
                        packet.data[channel - 1]
                        if channel <= len(packet.data)
                        else "N/A"
                        for channel in channels
                    ]
                    if values != last_values:
                        last_values = values
                        yield values
    finally:
        artnet.close()