from flask import Flask
import boto3

aws_access_key_id="ASIAUIOYHLNDJHQHHVMR"
aws_secret_access_key="j2xxFBqI05b1/xOWBH2z/MAvGtLw9KQ20V01YAq2"
aws_session_token="FwoGZXIvYXdzEBkaDO3ElrX1VRvM/EA+bCLAATb2mHVTfYNe2NqT0NBv9GIaXnarQm8Vby4cLYCPt2GbTkfsQFriVbgNKc1SbTEuxHX4KLoBT/vq3o2vZ6n2bKf6Yo65cqoJgLH7wW5343F5Lbv0L2Fy9oBxwgXAHrfNnHlbotvYnI9MPH2GQILPEdcjqcpm21lllBzihBrSN/eNGJ6F2csKiOAJ3PcEj4AP05LmQn26XIPobOdsmGs41aoE5LQzGdsLPLdey7vJQx+yrqnxGLajoQ6q/IydypTmfiiLhr2gBjItVDXiCb8qRrpxTBQgkEcS4xe3n3dmrRrZcgHyyv/jzUzh06/5TXZFvVhHq6zJ"
application = Flask(__name__)

def get_session():
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name='us-east-1'
    )
    return session

def get_dynamodb():
    session = get_session()
    dynamodb = session.client('dynamodb')
    return dynamodb

@application.route('/')
def main_entry():
    return "<p>Hello World! Flask app running on elastic beanstalk</>"

@application.route('/begin')
def begin_sudent_app_check():
    try:
        session = get_session()
        db_client = session.resource("dynamodb", region_name="us-east-1")
        table = db_client.Table('StudentActivity')
        table.put_item(Item={
            'Banner' : 'B00899369',
            'first_name' : 'Anirudh',
            'last_name' : 'Hosur',
            'age' : 23,
            'id' : 2
        })
        dynamodb = get_dynamodb()
        response = dynamodb.get_item(TableName="StudentActivity", Key={
            'Banner':{'S' : 'B00899369'}
            })
        return response['Item']
    except Exception as e:
        return "Fail" + str(e), 400
    
if __name__ == "__main__":
    application.run(port=5000, debug=True)
