import numpy as np

from game_send_inputs import restart_event
from typing import Dict
from f1_22_telemetry.listener import TelemetryListener
from f1_22_telemetry.packets import HEADER_FIELD_TO_PACKET_TYPE, Packet


def _get_listener():
    try:
        print('Starting listener on localhost:20777')
        return TelemetryListener()
    except OSError as exception:
        print(f'Unable to setup connection: {exception.args[1]}')
        print('Failed to open connector, stopping.')
        exit(127)


def get_car_infos(data):
    return {'speed': data['PacketCarTelemetryData'].to_dict()['car_telemetry_data'][0]['speed'],  # Vitesse
            'throttle': data['PacketCarTelemetryData'].to_dict()['car_telemetry_data'][0]['throttle'],  # Accélérateur
            'brake': data['PacketCarTelemetryData'].to_dict()['car_telemetry_data'][0]['brake']}  # Frein


def get_car_position(data):
    return {'x': data['PacketMotionData'].to_dict()['car_motion_data'][0]['world_position_x'],  # Position x
            'y': data['PacketMotionData'].to_dict()['car_motion_data'][0]['world_position_y'],  # Position y
            'z': data['PacketMotionData'].to_dict()['car_motion_data'][0]['world_position_z']}  # Position z


def get_lap_infos(data):
    return {'lap_time': data['PacketLapData'].to_dict()['lap_data'][0]['current_lap_time_in_ms'],
            # Durée du tour actuel en ms
            'lap_num': data['PacketLapData'].to_dict()['lap_data'][0]['current_lap_num'],  # Numéro du tour actuel
            'sector': data['PacketLapData'].to_dict()['lap_data'][0]['sector']}  # Numéro du secteur actuel


samples = {}
listener = _get_listener()
coords = ""

i = 0

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
        car_pos = get_car_position(samples)
        car_infos = get_car_infos(samples)
        lap = get_lap_infos(samples)
        surface = np.array(samples['PacketCarTelemetryData'].to_dict()['car_telemetry_data'][0]['surface_type'])
        # print(samples['PacketCarTelemetryData'].to_dict()['car_telemetry_data'][0]['speed'])
        print(f"x: {car_pos['x']}, "
              f"y: {car_pos['y']}, "
              f"z: {car_pos['z']}, "
              f"speed: {car_infos['speed']}"
              f"type: {surface}, "
              f"lap_time: {lap['lap_time']}, "
              f"lap_num: {lap['lap_num']}, "
              f"sector_num: {lap['sector']}, ")

        if surface.sum() > 4:
            print("Tu sors là !")
            restart_event()
            break

    except Exception as e:
        print('Response error : {}'.format(e))

    i += 1

    # if i == 5000:
    #     break

# with open(f'lap/first.csv', 'w') as fh:
#     fh.write(coords)
