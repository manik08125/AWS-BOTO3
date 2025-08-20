import boto3


client = boto3.client('ec2')

response = client.start_instances(
    InstanceIds=[
        'i-0f069f01c95bd409b',
    ],
)

print(response)