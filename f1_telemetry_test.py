import time
import copy
import json

from f1_22_telemetry.listener import TelemetryListener
from f1_22_telemetry.packets import HEADER_FIELD_TO_PACKET_TYPE


def _get_listener():
    try:
        print('Starting listener on localhost:20777')
        return TelemetryListener()
    except OSError as exception:
        print(f'Unable to setup connection: {exception.args[1]}')
        print('Failed to open connector, stopping.')
        exit(127)


samples = {}
listener = _get_listener()
packets_to_capture = copy.deepcopy(HEADER_FIELD_TO_PACKET_TYPE)

i = 0

in_file = []

while True:
    packet = listener.get()

    key = (
        packet.header.packet_format,
        packet.header.packet_version,
        packet.header.packet_id,
    )

    packet_type = HEADER_FIELD_TO_PACKET_TYPE[key].__name__

    samples[packet_type] = packet
    try:
        print(samples['PacketCarTelemetryData'].to_dict()['car_telemetry_data'][0]['speed'])
    except:
        print("No entry yet")
    # for packet_name, packet in samples.items():
    #     if packet_name == 'PacketCarTelemetryData':
    #         print(packet.to_dict()['car_telemetry_data'][0]['speed'])
    #         # print(packet_name)
    #         # print(packet.to_dict())
    #         if i == 0:
    #             start_time = time.time()
    #             in_file.append(packet.to_dict())
    #         if i == 1499:
    #             end_time = time.time()
    #             in_file.append(packet.to_dict())
    #
    #         i += 1
    #
    # if key in list(packets_to_capture):
    #     packet_type = HEADER_FIELD_TO_PACKET_TYPE[key].__name__
    #     samples[packet_type] = packet
    #     del packets_to_capture[key]

    # print('Done!')

# print("--- %s seconds ---" % (end_time - start_time))

# with open(f'json/PacketCarTelemetryData.json', 'a+') as fh:
#     json.dump(in_file, fh, indent=2)
# while True:
# print(packet2)
# time.sleep(1)
