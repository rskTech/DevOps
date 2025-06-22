import json
import boto3
import os
import urllib.parse

# Initialize SNS client
sns_client = boto3.client('sns')

# Environment variable for the SNS topic ARN
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

def lambda_handler(event, context):
    """
    Handles S3 put events and publishes a message to an SNS topic.
    """
    if not SNS_TOPIC_ARN:
        print("Error: SNS_TOPIC_ARN environment variable not set.")
        return {
            'statusCode': 500,
            'body': json.dumps('SNS_TOPIC_ARN environment variable not set')
        }

    print("Received event: " + json.dumps(event, indent=2))

    try:
        # Get the S3 bucket and object key from the event
        s3_event = event['Records'][0]['s3']
        bucket_name = s3_event['bucket']['name']
        object_key = urllib.parse.unquote_plus(s3_event['object']['key'], encoding='utf-8')

        subject = f"New file uploaded to S3 bucket: {bucket_name}"
        message = (
            f"A new file has been uploaded to your S3 bucket.\n\n"
            f"Bucket: {bucket_name}\n"
            f"File: {object_key}\n\n"
            f"Event details: {json.dumps(event['Records'][0], indent=2)}" # Includes more event details
        )

        print(f"Publishing message to SNS Topic: {SNS_TOPIC_ARN}")
        print(f"Subject: {subject}")
        print(f"Message: {message}")

        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject=subject
        )

        print("Message published successfully to SNS: " + json.dumps(response))
        return {
            'statusCode': 200,
            'body': json.dumps('Message published successfully to SNS')
        }

    except KeyError as e:
        print(f"Error: Missing expected key in S3 event: {e}")
        print("Full event structure:", json.dumps(event))
        return {
            'statusCode': 400,
            'body': json.dumps(f'Error processing S3 event: Missing key {e}')
        }
    except Exception as e:
        print(f"Error publishing to SNS: {e}")
        # Consider re-raising or specific error handling
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error publishing to SNS: {str(e)}')
        }

if __name__ == '__main__':
    # Example event for local testing (replace with a sample S3 event)
    example_event = {
      "Records": [
        {
          "eventVersion": "2.1",
          "eventSource": "aws:s3",
          "awsRegion": "us-east-1",
          "eventTime": "1970-01-01T00:00:00.000Z",
          "eventName": "ObjectCreated:Put",
          "userIdentity": {
            "principalId": "EXAMPLE"
          },
          "requestParameters": {
            "sourceIPAddress": "127.0.0.1"
          },
          "responseElements": {
            "x-amz-request-id": "EXAMPLE123456789",
            "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
          },
          "s3": {
            "s3SchemaVersion": "1.0",
            "configurationId": "testConfigRule",
            "bucket": {
              "name": "your-s3-bucket-name",
              "ownerIdentity": {
                "principalId": "EXAMPLE"
              },
              "arn": "arn:aws:s3:::your-s3-bucket-name"
            },
            "object": {
              "key": "HappyFace.jpg",
              "size": 1024,
              "eTag": "0123456789abcdef0123456789abcdef",
              "sequencer": "0A1B2C3D4E5F678901"
            }
          }
        }
      ]
    }
    # Set environment variable for local testing
    os.environ['SNS_TOPIC_ARN'] = 'arn:aws:sns:us-east-1:123456789012:YourSnsTopicName'
    lambda_handler(example_event, None)
