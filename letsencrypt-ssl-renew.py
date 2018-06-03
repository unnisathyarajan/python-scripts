#Script to renew SSL Certificates of Lets Encrpyt. 
#Before renewal it will use IAM ROLE to fetch temp creds for adding 443 to pulbic and revert the action once SSL is renewed. 

#!/usr/bin/python 
import boto3
import json
import urllib2
import subprocess

def main():

#Fetching tmp creds from IAM Role is enforced because the EC2 instance has .aws/config file with IAM creds and boto3 would pick up those creds as it has higher precendance over IAM Role.

 tmp_cred_url = "http://169.254.169.254/latest/meta-data/iam/security-credentials/myrolename/"
 response = urllib2.urlopen(tmp_cred_url)
 data = response.read()
 ACCESS_KEY = json.loads(data)['AccessKeyId']
 SECRET_KEY = json.loads(data)['SecretAccessKey']
 SESSION_TOKEN = json.loads(data)['Token']

 ec2 = boto3.resource('ec2', region_name="eu-west-1",aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY,aws_session_token=SESSION_TOKEN)
 security_group = ec2.SecurityGroup('sg-123456')

#Opening 443 to public
 try:
  security_group.authorize_ingress(IpProtocol="tcp",FromPort=443,ToPort=443,CidrIp="0.0.0.0/0")
 except:
  print "Error Adding SG Rule."

 p = subprocess.Popen(['/usr/local/bin/certbot-auto', 'renew', '--pre-hook', 'gitlab-ctl stop', '--post-hook', 'gitlab-ctl start'], stdout=subprocess.PIPE)
 output, err = p.communicate()
 print output

  
#Closing 443 to public
 try:
  security_group.revoke_ingress(IpProtocol="tcp",FromPort=443,ToPort=443,CidrIp="0.0.0.0/0")
 except:
  print "Error Deleting SG Rule." 









if __name__ == "__main__":
 main()





