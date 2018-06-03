#!/usr/bin/python 
__author__ = "unnisathya"
#boto3 >= v1.4.7 (pip freeze | grep boto3)
#To Upgrade $pip install --upgrade boto3
import argparse
import boto3

def main():
 parser = argparse.ArgumentParser()
 parser.add_argument("security_group",help="Example: sg-28f3ed4c")
 parser.add_argument("port_number",help="Example: 22")
 parser.add_argument("ip",help="Example: 192.168.1.1/32")
 parser.add_argument("region",help="Example: us-east-1")
 parser.add_argument("description",help="Example: unni-home-ip")

 args = parser.parse_args()

#Initialization
 ec2 = boto3.resource('ec2', region_name=args.region)
 security_group = ec2.SecurityGroup(args.security_group)

#Add the SG Rule
 response = security_group.authorize_ingress(
    IpPermissions=[
        {
            'FromPort': int(args.port_number),
            'IpProtocol': 'tcp',
            'IpRanges': [
                {
                    'CidrIp': args.ip,
                    'Description': args.description
                    
                }
            ],
            'ToPort': int(args.port_number),
        },
    ],
 )

#Checking return status
 if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
  print "Rule Added"
 else:
  print "Error Adding Rule"

#Logging IPs
 with open("IPList.txt",'a') as Tmpfile:
  Tmpfile.write(args.ip + '\n')

 

if __name__ == '__main__':

 main()

