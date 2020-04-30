# AWS Lambda Ping

We may want to ping an AWS EC2 instance.
I also don't want to launch an EC2 instance for ping monitoring.

AWS Lambda can now work in VPCs.
Being able to ping with AWS Lambda makes monitoring work easier.

However, there is currently no way to do an ICMP ping from within AWS Lambda. This is because the Lambda function cannot use raw sockets.

Here, we will implement a method of pinging without using ICMP.
See /lambda/lambda_function.py for details. I think it's easy to understand because it is a simple code.
- Use TCP SYN ACK.
- If the Server is down, "timed out" is returned.
- If the Server is alive, "Connection refused" is returned.

##  Usage:
1. Create a VPC and a test server.
```shell script
$ aws cloudformation create-stack \
--stack-name ping-test-vpc \
--region ap-northeast-1 \
--template-body file://vpc.yml \
--capabilities CAPABILITY_NAMED_IAM
```

2. Create an AWS Lambda function to ping.
```shell script

# Please specify the bucket name to upload the code of lambda function.
$ UPLOADBUCKETNAME=yagita-lambda-functions

$ aws cloudformation package \
    --template-file vpc-lambda.yml \
    --s3-bucket $UPLOADBUCKETNAME \
    --output-template-file packaged.yml

$ aws cloudformation deploy \
    --stack-name ping-vpc-lambda \
    --region ap-northeast-1 \
    --template-file packaged.yml \
    --capabilities CAPABILITY_NAMED_IAM \
    --output text
```

3. How to check: Run the Lambda Function with Test in the AWS Lambda console.

## Point
As in EC2SecurityGroupIngress (AWS :: EC2 :: SecurityGroupIngress) of  
vpc-lambda.yml, to receive pings from Lambda Function, please allow  
access from Lambda in the EC2 security group.

Also, in order to ping from a Lambda function in a different Subnet,  
it is necessary to set it in routing.

## Note
When deleting ping-vpc-lambda stack of Cloudformation,  
it may time out and the deletion may fail. In this case,  
manually deleting the ENI associated with the Lambda Function  
may resolve the issue.
