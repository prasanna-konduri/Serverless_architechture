import json
import boto3

INSTANCEID = 'i-054ad0107db37961e'
REGION = 'us-west-2'

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


def create_AMI(snapshot_id, instance):
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
        Name = "pk-auto-stop-AMI-From-Snapshot"
    )
    
    return image['ImageId']
    
    
def lambda_handler(event, context):
    instance = get_instance(INSTANCEID)
    volume_id = instance["BlockDeviceMappings"][0]['Ebs']['VolumeId']


    snapshots = ec2_client.describe_snapshots(
        Filters=[{'Name': 'volume-id', 'Values': [volume_id]}]
    )
    
    latest_snapshot = max(snapshots['Snapshots'], key=get_start_time)
    
    latest_snapshot_id = latest_snapshot['SnapshotId']
    
    ami_id = create_AMI(latest_snapshot_id,instance)
    
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

