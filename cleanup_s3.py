import boto3
from datetime import datetime, timezone, timedelta

LIMIT = 30
BUCKET_NAME = 'prasannabatch7'

s3 = boto3.client('s3')

def get_time(limit):
    now = datetime.now(timezone.utc)
    time_left = now- timedelta(days=limit)
    return time_left


def list_objects(bucket_name):

    response = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        return response['Contents']
    else:
        return None

def delete_files(bucket_name, objects, time_limit):
    deleted_files = []
    
    for object in objects:
        object_key = object['Key']
        object_last_modified = object['LastModified']
        
        if object_last_modified < time_limit:
            print(f"Deleting {object_key} (Last Modified: {object_last_modified})")
            s3.delete_object(Bucket=bucket_name, Key=object_key)
            deleted_files.append(object_key)
    
    return deleted_files

def lambda_handler(event, context):
    time_left= get_time(LIMIT)

    objects = list_objects(BUCKET_NAME)
    
    try:

        if objects is not None:
            
            deleted_files = delete_files(BUCKET_NAME, objects, time_left)
            
            if deleted_files:
                print(f"Deleted files: {deleted_files}")
                return {
                    'statusCode': 200,
                    'body': f"Deleted files: {deleted_files}"
                }
            else:
                print("No older files found.")
                return {
                    'statusCode': 200,
                    'body': "No older files found."
                }
        else:   
            print('Bucket {BUCKET_NAME} is empty');
            return {
                        'statusCode': 200,
                        'body': f"Bucket {BUCKET_NAME} is empty."
                    }

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"An error occurred: {str(e)}"
        }
