import subprocess


class NmapWrapper:
    NMAP_COMMAND = 'sudo nmap -p 22,80,445,65123,56123 -O 192.168.0.*'
    def __init__(self):
        pass

    def scan_network(self):
        """
        Scan 5 most important ports to detect an OS over an entire network
        Assumes that everyone will be under 192.168.0.*
        
        :return: None
        """
        result = subprocess.check_output(NmapWrapper.NMAP_COMMAND, shell=True)