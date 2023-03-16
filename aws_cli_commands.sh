aws ec2 run-instances \
--image-id ami-054cb116359624aa3 \
--count 1 \
--instance-type c6g.xlarge \
--block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":8,"VolumeType":"gp2","DeleteOnTermination":true}},{"DeviceName":"/dev/sdb","NoDevice":""},{"DeviceName":"/dev/sdc","NoDevice":""}]'

aws ec2 create-image \
--instance-id i-05edcf850576a8254 \
--name "ukv-umem(arm)" \
--block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"DeleteOnTermination":true}},{"DeviceName":"/dev/sdb","NoDevice":""},{"DeviceName":"/dev/sdc","NoDevice":""}]'

# Get ami status
aws ec2 describe-images --image-ids ami-0a59ee7ab97aaabeb --query 'Images[].State' --output json

# Create Folder in bucket
aws s3api put-object --bucket unum-cloud-wiki --key FolderNameInS3/ --acl bucket-owner-full-control --content-length 0
# Cp local folder
aws s3 cp LocalFolder/ s3://unum-cloud-wiki/WikiTest/ --recursive
# Sync local folder
aws s3 sync LocalFolder/ s3://unum-cloud-wiki/FolderName

# print s3 bucket folder files cound
aws s3 ls s3://unum-cloud-wiki/00000/ --summarize | grep "Total Objects:" | awk '{print $3}'

# Bucket permissions
{
    "Version": "2012-10-17",
    "Id": "Policy1678161186202",
    "Statement": [
        {
            "Sid": "Stmt1678161171069",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::495295622846:root",
                    "arn:aws:iam::679383340927:root"
                ]
            },
            "Action": [
                "s3:ListBucket",
                "s3:DeleteObject",
                "s3:GetObject",
                "s3:PutObject",
                "s3:RestoreObject"
            ],
            "Resource": [
                "arn:aws:s3:::unum-cloud-wiki/*",
                "arn:aws:s3:::unum-cloud-wiki"
            ]
        }
    ]
}
