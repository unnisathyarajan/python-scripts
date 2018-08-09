# python-scripts

Some quick python scripts useful for DevOps/Sysadmin tasks.

a)aws_security_groups_cli_update/authorize-sg.py
----------------------------------------------
To add/authorize a rule in a security group.

#### Configuration

[Configure AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)

#### Prequisite
* boto3 >= v1.4.7
* python 2.7

**Usage:**
```
./authorize-sg.py --help
usage: authorize-sg.py [-h] security_group port_number ip region description

positional arguments:
  security_group  Example: sg-28f3ed4c
  port_number     Example: 22
  ip              Example: 192.168.1.1/32
  region          Example: us-east-1
  description     Example: unni-home-ip

optional arguments:
  -h, --help      show this help message and exit

```

**Example:**
```
./authorize-sg.py sg-821c91n4 80 34.250.77.12/32 us-east-1 my-public-ip
```

b)aws_security_groups_cli_update/revoke-sg.py
-------------------------------------------
To delete/revoke a rule in a security group. (rest is same as above.)



c)mongodb-backup.py
-------------------------------------------
To take mongodb dump and upload to S3 bucket.
The access key and secret key is not required if the script is been executed in an EC2 instance with a role associated that has S3 upload permissions.

**Usage:**

```
./mongodb-backup.py --help
usage: mongodb-backup.py [-h] [--ak AK] [--sk SK] [--dir [DIR]]
                         [--s3bucket S3BUCKET] [--dbname DBNAME] [--ret [RET]]

optional arguments:
  -h, --help                     show this help message and exit
  --ak AK (optional)             Access Key (ak), Example: KKIAJNXOI3GW3MLVIULN
  --sk SK (optional)             Secret Key (sk), Example: fg3iubaaLDpNiz0swzgHaL
  --dir [DIR]                    Dump Directory, Default: /mongodb-snapshot
  --s3bucket S3BUCKET            S3 bucket name, Example: mongodb-backup-bucket
  --dbname DBNAME                MongoDB database name, Example: myappdb
  --ret [RET] (optional)         Retention in days, Default: 7 (7 days of backup will be
                                 retained without deletion)
```

**Example:**
```
./mongodb-backup.py --s3bucket mongodb-backup-bucket --ret 10 --dbname myapp
```


d)uploader.py
-------------------------------------------
Script to copy images without gzip header while the sync uploads all files with gzip header. It is used as a side script in CI/CD pipeline job.

**Usage:**

```
./uploader.py . bucketname/dir/
Argument #1 : to mention the source path
Argument #2 : bucket name and directory with a trailing /
```
