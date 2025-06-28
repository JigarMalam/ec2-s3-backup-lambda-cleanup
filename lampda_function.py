import boto3
import datetime

s3 = boto3.client('s3')

BUCKET_NAME = 'ec2-daily-backup-s3'
PREFIX = 'backups/'  
RETENTION_DAYS = 0

def lambda_handler(event, context):
    now = datetime.datetime.now(datetime.timezone.utc)
    deleted = []

    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX)
    print("S3 Objects:", response)
    if 'Contents' not in response:
        return {'message': 'No files found'}

    for obj in response['Contents']:
        age = (now - obj['LastModified']).days
        if age > RETENTION_DAYS:
            s3.delete_object(Bucket=BUCKET_NAME, Key=obj['Key'])
            deleted.append(obj['Key'])

    return {
        'deleted_files': deleted,
        'status': 'Cleanup completed'
    }
