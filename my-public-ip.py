#!/usr/bin/python 
__author__ = "unnisathya"
from urllib2 import urlopen

def main():

 my_public_ip=urlopen('http://ip.42.pl/raw').read()
 cidr=my_public_ip + str("/32")
 print "Your Public IP: " + cidr 













if __name__ == "__main__":
 main()

