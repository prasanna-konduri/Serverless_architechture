import json
import boto3
from datetime import datetime, timezone, timedelta

VOLUMEID = 'vol-06e452fe34c7736d5'
REGION = 'us-west-2'
LIMIT = 30

ec2_client = boto3.client('ec2', region_name=REGION)

def get_start_time(snapshot):
    return snapshot['StartTime']

def get_time(limit):
    now = datetime.now(timezone.utc)
    time_left = now- timedelta(days=limit)
    return time_left

def create_snapshot(volume_id,description):
    snapshot = ec2_client.create_snapshot(VolumeId=volume_id, Description=description)
    return snapshot

def delete_snapshot(snapshot_id):
    response = ec2_client.delete_snapshot(
        SnapshotId=snapshot_id,
        DryRun=True|False
    )
    return snapshot_id

def get_snapshots(volume_id):
    snapshots = ec2_client.describe_snapshots(
        Filters=[{'Name': 'volume-id', 'Values': [volume_id]}]
    )
    return snapshots['Snapshots']


def lambda_handler(event, context):
    deleted_ids = []
    message = []
    #create snapshot
    snapshot = create_snapshot(VOLUMEID,'automated snapshot of pk-auto-stop instance')
    created_id = snapshot['SnapshotId']
    if created_id:
        message.append({"created_id": created_id})
        
    print(f"snapshot created with id: {created_id}")
    #get list of snapshots attached to a volume
    snapshots = get_snapshots(VOLUMEID)
    
    time_left = get_time(LIMIT)
    for snapshot in snapshots:
        start_time = get_start_time(snapshot)
        
        if start_time<time_left:
            #delete a snapshot
            delete_id = delete_snapshot(snapshot['SnapshotId'])
            print(f"old snapshot deleted with Id: {delete_id}")
            deleted_ids.append(delete_id )
        else:
            print(f"snapshots are less than 30 days old")
            
        
        if deleted_ids:
            message.append({"deleted_ids":deleted_ids})

    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }
