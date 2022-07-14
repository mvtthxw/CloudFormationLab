AWS VPC

Paramentes:
-Env
-CIDR

Resources:
1. VPC
-3 AZ
-Public and private subnets
-RTs
-Public, private and SessionMaganer SG
-Without NAT and IGW

2. S3 bucket
-versioning
-S3 encryption

3. EC2
-amazon linux 2
-EC2 role - permission for Session Manager and download file from S3 only 
-security group
-encrypted volume
-VPC Endpoints for Session Manager



Useful link for Session Manager:
https://aws.amazon.com/blogs/mt/automated-configuration-of-session-manager-without-an-internet-gateway/ 