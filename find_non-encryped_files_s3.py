import boto3
import json

s3_client = boto3.client('s3') 
buckets_with_noencryption = []

def list_buckets():
    response = s3_client.list_buckets()
    return response['Buckets']

def get_bucket_encryption(bucket_name):
    try:
        response = s3_client.get_bucket_encryption(Bucket=bucket_name)
        rules = response['ServerSideEncryptionConfiguration']['Rules']

        if not rules:
            return False

        for rule in rules:
            sse_type = rule['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
            if sse_type == 'aws:kms':
                kms_key_id = rule['ApplyServerSideEncryptionByDefault'].get('KMSMasterKeyID', 'Default KMS Key')
                print(f"Bucket '{bucket_name}' is encrypted with KMS using Key ID: {kms_key_id}")
            else:
                print(f"Bucket '{bucket_name}' is encrypted with {sse_type}")

        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
            print(f"Bucket '{bucket_name}' does not have server-side encryption enabled.")
        else:
            print(f"Error fetching configuration for bucket {bucket_name}: {e}")




def lambda_handler(event, context):
    buckets = list_buckets()
    for bucket in buckets:
       enc_state =  get_bucket_encryption(bucket['Name'])
       if not enc_state:
           buckets_with_noencryption.append(bucket['Name'])
          
    if not buckets_with_noencryption:
        message = "All buckets have serverside encryption"
    else:
        message = f"the names of buckets with no serverside encryption: {buckets_with_noencryption}"
    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }
