import numpy as np

from game_events import restart_event
from f1_22_telemetry.listener import TelemetryListener
from f1_22_telemetry.packets import HEADER_FIELD_TO_PACKET_TYPE, Packet


def get_listener():
    try:
        print('Starting listener on localhost:20777')
        return TelemetryListener()
    except OSError as exception:
        print(f'Unable to setup connection: {exception.args[1]}')
        print('Failed to open connector, stopping.')
        exit(127)


def get_car_infos(data):
    return {'speed': data['PacketCarTelemetryData'].car_telemetry_data[0].speed,  # Vitesse
            'throttle': data['PacketCarTelemetryData'].car_telemetry_data[0].throttle,  # Accélérateur
            'brake': data['PacketCarTelemetryData'].car_telemetry_data[0].brake}  # Frein


def get_car_position(data):
    return {'x': data['PacketMotionData'].car_motion_data[0].world_position_x,  # Position x
            'y': data['PacketMotionData'].car_motion_data[0].world_position_y,  # Position y
            'z': data['PacketMotionData'].car_motion_data[0].world_position_z}  # Position z


def get_lap_infos(data):
    return {'lap_time': data['PacketLapData'].lap_data[0].current_lap_time_in_ms,   # Durée du tour actuel en ms
            'lap_num': data['PacketLapData'].lap_data[0].current_lap_num,  # Numéro du tour actuel
            'sector': data['PacketLapData'].lap_data[0].sector}  # Numéro du secteur actuel


if __name__ == '__main__':

    listener = get_listener()
    samples = {}
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
            car_infos = get_car_infos(samples)
            print(f"speed: {car_infos['speed']} "
                  f"throttle: {car_infos['throttle']} "
                  f"brake: {car_infos['brake']}")

        except Exception as e:
            pass

# if __name__ == '__main__':
#     samples = {}
#     listener = _get_listener()
#     coords = ""
#
#     i = 0
#
#     while True:
#         packet = listener.get()
#
#         key = (
#             packet.header.packet_format,
#             packet.header.packet_version,
#             packet.header.packet_id,
#         )
#
#         packet_type = HEADER_FIELD_TO_PACKET_TYPE[key].__name__
#
#         samples[packet_type] = packet
#         try:
#             car_pos = get_car_position(samples)
#             car_infos = get_car_infos(samples)
#             lap = get_lap_infos(samples)
#             surface = np.array(samples['PacketCarTelemetryData'].to_dict()['car_telemetry_data'][0]['surface_type'])
#             # print(samples['PacketCarTelemetryData'].to_dict()['car_telemetry_data'][0]['speed'])
#             print(f"x: {car_pos['x']}, "
#                   f"y: {car_pos['y']}, "
#                   f"z: {car_pos['z']}, "
#                   f"speed: {car_infos['speed']}"
#                   f"type: {surface}, "
#                   f"lap_time: {lap['lap_time']}, "
#                   f"lap_num: {lap['lap_num']}, "
#                   f"sector_num: {lap['sector']}, ")
#
#             if surface.sum() > 4:
#                 print("Tu sors là !")
#                 restart_event()
#                 break
#
#         except Exception as e:
#             print('Response error : {}'.format(e))
#
#         i += 1
