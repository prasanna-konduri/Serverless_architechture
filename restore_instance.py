import json
import boto3

INSTANCEID = 'i-054ad0107db37961e'
REGION = 'us-west-2'
AMI_BASE_NAME = "pk_auto_stop_snapshot_AMI"


ec2_client = boto3.client('ec2', region_name=REGION) 

def get_instance(instance_id):
   response = ec2_client.describe_instances(
        InstanceIds=[
        instance_id,
        ]
    )
   for reservation in response['Reservations']:
       instances = reservation['Instances'] 
   return instances[0]

def get_start_time(snapshot):
    return snapshot['StartTime']

def check_image_exists(ami_name):
    response = ec2_client.describe_images(
        Filters=[
            {'Name': 'name', 'Values': [ami_name]},
            {'Name': 'state', 'Values': ['available']}
        ],
        Owners=['self']
    )
    return response

def create_AMI(snapshot_id, instance, ami_name):
    image = ec2_client.register_image(
        Architecture = instance['Architecture'],
        VirtualizationType = instance['VirtualizationType'],
        BlockDeviceMappings = [
            {
                'DeviceName': instance["BlockDeviceMappings"][0]['DeviceName'],
                'Ebs': {
                    'SnapshotId': snapshot_id,
                    'DeleteOnTermination': True
                }
           }
        ],
        RootDeviceName = instance['RootDeviceName'],
        Name = ami_name
    )
    
    return image['ImageId']
    
    
def lambda_handler(event, context):
    instance = get_instance(INSTANCEID)
    volume_id = instance["BlockDeviceMappings"][0]['Ebs']['VolumeId']
    ami_name = AMI_BASE_NAME
    
    snapshots = ec2_client.describe_snapshots(
        Filters=[{'Name': 'volume-id', 'Values': [volume_id]}]
    )
    
    latest_snapshot = max(snapshots['Snapshots'], key=get_start_time)
    
    latest_snapshot_id = latest_snapshot['SnapshotId']
    
    print(f"latest snapshot id: {latest_snapshot_id}")
    
    for i in range(11):
        ami_name = AMI_BASE_NAME+str(i)
        print(f"checking if the image exists with name: {ami_name}")
        response = check_image_exists(ami_name)
        if not response['Images']:
         break
          
    
    ami_id = create_AMI(latest_snapshot_id,instance,ami_name)
    print(f'AMI created with image id: {ami_id}')

    
    new_instance = ec2_client.run_instances(
                ImageId=ami_id,
                InstanceType=instance['InstanceType'],
                MinCount=1,
                MaxCount=1      
            )
    
    return {
            'statusCode': 200,
            'body': json.dumps(f"New Instance created with instance id: {new_instance['Instances'][0]['InstanceId']}")
        }

