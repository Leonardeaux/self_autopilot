import time
from ctypes import *
from f1_22_telemetry.listener import TelemetryListener
from f1_22_telemetry.packets import PacketMotionData, PacketHeader, PacketCarDamageData, HEADER_FIELD_TO_PACKET_TYPE


class TelemetryListenerCar(TelemetryListener):

    def __init__(self, port, host):
        super().__init__(host, port)

    def get(self):
        packet_so = self.socket.recv(2048)
        header = PacketMotionData.from_buffer_copy(packet_so)

        key = (header.header.packet_format, header.header.packet_version, header.header.packet_id)
        print(key)
        return HEADER_FIELD_TO_PACKET_TYPE[key].unpack(packet_so)


listener = TelemetryListenerCar(port=20777, host='localhost')
packet2 = listener.get()

# while True:
# print(packet2)
    # time.sleep(1)
