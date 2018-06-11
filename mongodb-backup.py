#!/usr/bin/python3
__author__ = "unnisathya"

import argparse
import boto3
import os
from datetime import date
import subprocess
import shutil
import time



def s3_upload(access_keys,secret_keys,source_file,dest_s3_obj_name,bucket_name):
 if access_keys is not None or secret_keys is not None:
  s3 = boto3.resource('s3',aws_access_key_id=access_keys, aws_secret_access_key=secret_keys)
  print("S3 Connection Established")
 else:
  print("No keys provided, fetching keys from EC2 role.")
  s3 = boto3.resource('s3')
  print("S3 Connection established using EC2 role.")
  
 	
 print("Uploading to S3 bucket: "+ bucket_name +" ... ")
 s3.meta.client.upload_file(source_file, bucket_name, dest_s3_obj_name)
 


def mongodb_backup(dump_dir,database_name):
 snap_date = date.today().isoformat()
#Create dump directory
 if not os.path.exists(dump_dir):
  os.makedirs(dump_dir)
  print("Backup directory created!")
 
#Mongodump Command
 try:
  return_stat = subprocess.call(['/usr/bin/mongodump','--db', database_name ,'--out',dump_dir])
 except:
  print("Error! Failed to talk mongodump")
 
#Append date with dump directory name
 dump_dir_snap_name= dump_dir +"/"+database_name+"-"+ str(snap_date)
 

 if not return_stat:
   if not os.path.exists(dump_dir_snap_name):
    os.renames(dump_dir+"/talk",dump_dir_snap_name)
   #shutil.make_archive(dump_dir_snap_name,'zip',dump_dir_snap_name,dump_dir_snap_name)
#Create a zip file of the dump directory for upload
   shutil.make_archive(dump_dir_snap_name,'zip',dump_dir_snap_name)
   print("Zip file created")
   return(dump_dir_snap_name+".zip")



def cleanup(retention_period_days,directory):
 current_time = time.time()
 for single_file in os.listdir(directory):
  file_path = directory+"/"+single_file
  creation_time = os.path.getctime(file_path)
 if (current_time - creation_time) // (24 * 3600) >= retention_period_days:
  print("File older than "+ str(retention_period_days) +" days "+single_file)
  os.unlink(single_file)


   

def main():

 parser =  argparse.ArgumentParser()
 parser.add_argument("--ak", help="Access Key (ak), Example: KKIAJNXOI3GW3MLVIULN")
 parser.add_argument("--sk", help="Secret Key (sk), Example: fg3iubaaLDpNiz0swzgHaL")
 parser.add_argument("--dir", help="Dump Directory, Default: /mongodb-snapshot", nargs='?', default="/mongodb-snapshot")
 parser.add_argument("--s3bucket", help="S3 bucket name, Example: mongodb-backup-bucket")
 parser.add_argument("--dbname", help="MongoDB database name, Example: myappdb")
 parser.add_argument("--ret", help="Retention in days, Default: 7 (7 days of backup will be retained without deletion)", nargs='?', type=int, default=7)
 args = parser.parse_args()


#S3 Argument mandatory
 if args.s3bucket:
  bucket_name=args.s3bucket
 else:
  print("Please specify S3 Bucket")
  exit()

#MongoDB DB name mandatory
 if not args.dbname: 
  print("Please specify MongoDB database name")
  exit()

#MongoDB Backup Function
 zip_name = mongodb_backup(args.dir,args.dbname)
 s3_oject_name = zip_name.split("/")[2]

#Upload to S3 Bucket
 s3_upload(args.ak,args.sk,zip_name,s3_oject_name,bucket_name)

#Cleanup
 cleanup(args.ret,args.dir)









if __name__ == '__main__':
 main()