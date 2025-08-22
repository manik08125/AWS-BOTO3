import boto3

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    sns_client = boto3.client('sns')

    # ✅ FIXED ARN (quotes match properly)
    sns_topic_arn = "arn:aws:sns:us-east-1:115005006316:ebs"

    try:
        # Describe all EBS volumes
        volumes = ec2_client.describe_volumes()

        deleted_volumes = []
        skipped_volumes = []

        for vol in volumes['Volumes']:
            vol_id = vol['VolumeId']
            state = vol['State']

            if state == 'available':
                try:
                    ec2_client.delete_volume(VolumeId=vol_id)
                    deleted_volumes.append(vol_id)
                except Exception as e:
                    skipped_volumes.append(f"{vol_id} (delete failed: {str(e)})")
            else:
                skipped_volumes.append(f"{vol_id} (state={state}, not deleted)")

        # Build SNS message
        message = "📢 EBS Volume Cleanup Report\n\n"
        if deleted_volumes:
            message += "✅ Deleted Volumes:\n" + "\n".join(deleted_volumes) + "\n\n"
        if skipped_volumes:
            message += "⚠️ Skipped Volumes:\n" + "\n".join(skipped_volumes) + "\n\n"
        if not deleted_volumes and not skipped_volumes:
            message += "No volumes found.\n"

        sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject="EBS Volume Cleanup Report",
            Message=message
        )

        return {
            'statusCode': 200,
            'body': message
        }

    except Exception as e:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject="EBS Cleanup Failed",
            Message=f"Error describing/deleting volumes: {str(e)}"
        )
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
