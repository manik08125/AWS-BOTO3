import boto3


client = boto3.client('s3')

response = client.create_bucket(
    ACL='private',
    Bucket='boto3-first-s3-bucket-20aug',
    CreateBucketConfiguration={
        'LocationConstraint': 'us-east-1'
    }

)