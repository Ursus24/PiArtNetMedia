
from load import load_config
from python_artnet import Artnet

def receive_dmx():

    channel, universe, bind_ip = load_config()
    channels = list(range(channel, channel + 10))

    artnet = Artnet(bind_ip)
    last_values = None

    try:
        while True:
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
    except KeyboardInterrupt:
        return
    finally:
        artnet.close()