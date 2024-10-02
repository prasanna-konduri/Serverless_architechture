import json
import boto3

ec2_client = boto3.client('ec2', region_name='us-west-2') 
TAG = "Action"
START_TAG = "pk_autostart"
STOP_TAG = "pk_autostop"

def get_instances_by_tag(tag,value):
    instances = []
    response = ec2_client.describe_instances(Filters=[
        {
            'Name': f'tag:{tag}',
            'Values': [
                value,
            ]
        },
    ])
    reservations = response['Reservations']

    for reservation in reservations :
        for instance in reservation['Instances']:
            data = {
                'instance_id':instance['InstanceId'],
                'state': instance['State']['Name']
                }
        instances.append(data)
    print(instances)
    return instances; 
   
    
def change_instance_state (state, instance_ids):
    if(instance_ids):
        if(state == "start"):
            print(f"Starting instances: {instance_ids}")
            ec2_client.start_instances(InstanceIds=instance_ids)
            
        if(state == "stop"):
            print(f"Stoping instances: {instance_ids}")
            ec2_client.stop_instances(InstanceIds=instance_ids)
        

def lambda_handler(event, context):
    start_ids = []
    stop_ids = []
    #get all the instances with start
    start_instances =  get_instances_by_tag("Action","auto-start")
    for instance in start_instances:
        if(instance['state']!='running'):
            start_ids.append(instance['instance_id'])
    
    change_instance_state('start',start_ids)

    stop_instances = get_instances_by_tag("Action","auto-stop")
    for instance in stop_instances:
        if(instance['state']=='running'):
            stop_ids.append(instance['instance_id'])
    
    change_instance_state('stop',stop_ids)


    return {
        'statusCode': 200,
        'body': json.dumps({'stop_ids':stop_ids,'start_ids':start_ids})
    }
