# Serverless architechture
##Assignment 1: Automated Instance Management Using AWS Lambda and Boto3 
###Task: To automate the stopping and starting of EC2 instances based on tags.
1. Created two EC2 instances one instance named pk-auto-start with tag name "Action" and value "auto-start" and the other instance named pk-auto-stop with tag name "Action" and value "auto-stop".
2. After creating the instances initially kept auto-start instance in stopped state and auto-stop instance in running state.
   <img width="1440" alt="Screenshot 2024-10-02 at 1 08 14 PM" src="https://github.com/user-attachments/assets/7f6fcf61-8482-468a-a196-7254e387de65">
   
3. Created a IAM role "pk-EC2-full-access" with policies "AmazonEC2FullAccess" and "AWSLambdaBasicExecutionRole".
   <img width="1440" alt="Screenshot 2024-10-02 at 1 50 27 PM" src="https://github.com/user-attachments/assets/b2ba243b-1ee0-43a2-bbc3-2c9ed6d26c1c">

4. Created a lambda function "pk-EC2-auto-start-stop" with py3.10 as runtime, attached the above created role.
5. The script to execute the lambda function is attached in the python file [lambda_auto_start_stop.py](https://github.com/prasanna-konduri/serverless_architechture/blob/main/lambda_auto_start_stop.py)
6. Tested the function the execution results are attached in the below sreenshot.
   <img width="1440" alt="Screenshot 2024-10-02 at 1 09 39 PM" src="https://github.com/user-attachments/assets/c965e871-28fb-400a-840f-2525c00dcd6e">
   
7. The EC2 instances acted as expected through the lambda funtion execution.
   <img width="1440" alt="Screenshot 2024-10-02 at 1 33 36 PM" src="https://github.com/user-attachments/assets/aa46bf86-faa7-4482-983b-4d7c9ba8a377">

##Assignment 17: Restore EC2 Instance from Snapshot

###Objective: Automate the process of creating a new EC2 instance from the latest snapshot using a Lambda function.

1. Created a Lambda function named "restore-from-snapshot" with python 3.10 as runtime and pk-EC2-full-access as role attached to it.


2. Python code for fetching the latest snapshot and creating an EC2 instance is in [restore_instance.py](https://github.com/prasanna-konduri/serverless_architechture/blob/main/restore_instance.py)

3. The output for this lambda function when manually invoked is as follows.
   <img width="1440" alt="Screenshot 2024-10-03 at 4 07 06 AM" src="https://github.com/user-attachments/assets/e655d9ea-9852-47b8-86c3-133f552ba8de">
   
   <img width="1440" alt="Screenshot 2024-10-03 at 4 13 27 AM" src="https://github.com/user-attachments/assets/66fea9c3-82d3-45f2-91fb-9932ce49be03">
   
   <img width="1440" alt="Screenshot 2024-10-03 at 4 15 27 AM" src="https://github.com/user-attachments/assets/21b4e7a4-35fd-4845-b549-263d6a616799">




 
