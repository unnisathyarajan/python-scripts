#!/usr/bin/python3

"""
Script to copy images without gzip header while the sync uploads all files with gzip header. It is used as a side script in CI/CD pipeline job.
"""

import sys
import os
import re
import subprocess
from glob import glob




def get_all_files(path):
    #Recursively get list of all files
    allfiles = [y for x in os.walk(path) for y in glob(os.path.join(x[0], "*"))]
    return(allfiles)




def sync_all(scan_path,s3bucket):
    subprocess.call(["aws", "s3", "sync", scan_path, s3bucket, "--exclude", "\".git*\"", "--acl", "public-read", "--cache-control", "max-age=604800", "--content-encoding", "gzip"])
    print("SYNC COMPLETE")



def remove_image_gzip_header(filelist,extensions,s3bucket):
    for ext in extensions:
        exp = "\."+ext+"$"
        for file in filelist:
            if re.search(exp,file):
                s3destPath = s3bucket + file[2:]
                subprocess.call(["aws","s3","cp", file , s3destPath, "--acl", "public-read", "--cache-control", "max-age=604800"])
    print("IMAGE GZIP HEADER REMOVED")











def main():
    extensions = ["png","jpg","gif","JPG","PNG","GIF","svg","SVG","tif","TIF"]
    scan_path = sys.argv[1]
    bucket = sys.argv[2]
    if not re.search(r'[a-zA-z-.]+/[a-zA-z-.]+/',sys.argv[2]):
        print("put bucketname/dir/ with a trailing /")
        exit()


    s3bucket = "s3://"+ bucket
    files = get_all_files(scan_path)
    sync_all(scan_path,s3bucket)
    remove_image_gzip_header(files,extensions,s3bucket)


if __name__ == '__main__':
    main()
