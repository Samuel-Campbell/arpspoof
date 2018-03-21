import subprocess
import re


class NmapWrapper:
    ip_addr_regex = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    router_regex = re.compile('Nmap scan report for gateway')
    NMAP_COMMAND = 'sudo nmap -p 22,80,445,65123,56123 -O 192.168.0.*'

    def __init__(self):
        self.router_ip = None
        self.target_ip = []

    def scan_network(self):
        """
        Scan 5 most important ports to detect an OS over an entire network
        Assumes that everyone will be under 192.168.0.*
        
        :return: None
        """
        print("[+] Scanning network using nmap")
        result = subprocess.check_output(NmapWrapper.NMAP_COMMAND, shell=True).decode('utf-8')
        result = result.split('\n')
        for line in result:
            if re.search(self.router_regex, line):
                ip = re.search(self.ip_addr_regex, line).group(0)
                print("\t*Router found with ip {}".format(ip))
                self.router_ip = ip

            elif re.search(self.ip_addr_regex, line):
                ip = re.search(self.ip_addr_regex, line).group(0)
                print("\t*Target found with ip {}".format(ip))
                self.target_ip.append(ip)


if __name__ == '__main__':
    nmap = NmapWrapper()
    nmap.scan_network()