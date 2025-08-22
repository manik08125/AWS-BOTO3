import boto3

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')

  
    ami_id = "ami-0e325e1439f20b6c2"

    try:
        response = ec2_client.deregister_image(ImageId=ami_id)
        return {
            'statusCode': 200,
            'body': f'Successfully deregistered AMI {ami_id}',
            'response': response
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error deregistering AMI {ami_id}: {str(e)}'
        }
