#!/usr/bin/python
import subprocess
import argparse
from prometheus_client import Summary
from prometheus_client import start_http_server, Gauge
import random
import time


def bandwidth_measure_metric(server_ip,server_port):
    '''
    Returns current network bandwidth in Mbps
    '''
    try:
        p = subprocess.Popen(['/usr/bin/iperf', '-c', server_ip],stdout=subprocess.PIPE)
    except:
        print("iperf command could not be executed")


    out , err = p.communicate()
    return(out.split()[37])



def prom_export_metrics(server_ip,server_port):
    metric = Gauge('bandwidth_measure', 'Current network bandwidth')
    metric.set_function(lambda: bandwidth_measure_metric(server_ip,server_port))

    #To run as process
    @metric.time()
    def process_request(t):
        """A dummy function that takes some time."""
        time.sleep(t)

    while True:
        process_request(random.random())






def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", help="IP address of iperf server")
    parser.add_argument("--port",help="port number the iperf server is listening",default=5001)
    args = parser.parse_args()



#IP Argument mandatory
    if args.ip:
      server_ip=args.ip
    else:
      print("Please specify Iperf Server IP")
      exit()


    start_http_server(8000)
    prom_export_metrics(args.ip,args.port)








if __name__ == '__main__':
    main()
