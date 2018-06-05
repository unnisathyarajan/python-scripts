# python-scripts

Some quick python scripts useful for DevOps/Sysadmin tasks.

aws_security_groups_cli_update/authorize-sg.py
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

aws_security_groups_cli_update/revoke-sg.py
-------------------------------------------
To delete/revoke a rule in a security group.