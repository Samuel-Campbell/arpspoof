import pyshark
from main.util.file import File


class PysharkWrapper:

    """
    Protocol:
    {'ssdp', 'fake-field-wrapper', 'dns', 'ssl', 'quic', 'eth', 'ip', 'arp', 'ajp13', '_ws.malformed', 'udp', 'tcp'}
    """

    def __init__(self, wifi_location, target_ip):
        self.wifi_location = wifi_location
        self.target_ip = target_ip

    def capture(self, timeout=60):
        """
        Captures packets for n amount of time in seconds

        :param timeout: int
        :return: None
        """
        print('[+] Capturing Packets')
        capture = pyshark.LiveCapture()
        capture.sniff(timeout=timeout)
        self.__save_packets(capture)

    def __save_packets(self, capture):
        """
        [
            {
                type: udp,
                fields: ip_src, ip_dst...
            },
            {
                type: udp,
                fields: ip_src, ip_dst...
            }
        ]

        :param directory: string
        :param capture: pyshark.capture.capture.Capture()
        :return: None
        """
        print("[+] Saving packets")
        packet_list = []
        for i in range(len(capture)):
            packet_list.append(capture.next_packet())

        capture_list = []
        for packet in packet_list:
            for protocol in packet:
                packet_dict = {
                    'type': protocol._layer_name,
                    'fields': protocol._all_fields
                }
                capture_list.append(packet_dict)

        File.save_binary(self.wifi_location, self.target_ip + '.bin', capture_list)


if __name__ == '__main__':
    ps = PysharkWrapper('home', '192.168.0.100')
    ps.capture(15)