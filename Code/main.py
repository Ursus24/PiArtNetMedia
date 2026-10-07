from artnet import receive_dmx


def main():
    for dmx_values in receive_dmx():
        print(dmx_values)

main()