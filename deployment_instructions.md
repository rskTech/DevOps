# AWS Lambda S3 to SNS Notification: Deployment Instructions

This guide explains how to deploy and configure an AWS Lambda function that sends an email notification via SNS when a new file is uploaded to an S3 bucket.

You should have two files from the previous steps:
1.  `s3_to_sns_lambda.py`: The Python code for the Lambda function.
2.  `lambda_iam_policy.json`: The IAM policy document for the Lambda's execution role.

## 1. Create an SNS Topic and Subscription

1.  **Navigate to SNS:** Open the AWS Management Console and go to the SNS (Simple Notification Service) dashboard.
2.  **Create Topic:**
    *   Click on "Topics" in the left navigation pane.
    *   Click "Create topic".
    *   Choose "Standard" for the type.
    *   **Name:** Give your topic a descriptive name (e.g., `s3-new-file-notifications`).
    *   Leave other settings as default unless you have specific requirements.
    *   Click "Create topic".
3.  **Copy Topic ARN:** Once created, copy the **Topic ARN**. You will need this later for the Lambda environment variable and potentially for tightening IAM permissions.
4.  **Create Subscription:**
    *   With the new topic selected, click on the "Subscriptions" tab below the topic details.
    *   Click "Create subscription".
    *   **Protocol:** Select "Email".
    *   **Endpoint:** Enter the email address where you want to receive notifications.
    *   Click "Create subscription".
5.  **Confirm Subscription:** Check your email inbox for a message from AWS Notification. Click the link in the email to confirm your subscription. The subscription status should change to "Confirmed".

## 2. Create an IAM Role for Lambda

1.  **Navigate to IAM:** Go to the IAM (Identity and Access Management) dashboard in the AWS Console.
2.  **Create Role:**
    *   Click on "Roles" in the left navigation pane.
    *   Click "Create role".
    *   **Trusted entity type:** Select "AWS service".
    *   **Use case:** Select "Lambda".
    *   Click "Next".
3.  **Add Permissions:**
    *   Click "Create policy". This will open a new tab.
        *   In the policy editor, select the "JSON" tab.
        *   Open the `lambda_iam_policy.json` file you created earlier.
        *   Copy its content and paste it into the JSON editor in the AWS console, replacing the default content.
        *   **Important for Security:** Modify the SNS `Resource` in the policy. Replace `"*"` with the specific **SNS Topic ARN** you copied in Step 1.
            ```json
            // ... other policy parts ...
            {
                "Effect": "Allow",
                "Action": "sns:Publish",
                "Resource": "YOUR_SNS_TOPIC_ARN" // <-- PASTE YOUR SNS TOPIC ARN HERE
            }
            // ... other policy parts ...
            ```
        *   Click "Next: Tags".
        *   Click "Next: Review".
        *   **Policy Name:** Give the policy a descriptive name (e.g., `LambdaS3toSNSPolicy`).
        *   Click "Create policy".
    *   Close the policy creation tab and return to the "Create role" tab.
    *   Click the refresh button next to "Create policy".
    *   Search for the policy you just created (e.g., `LambdaS3toSNSPolicy`).
    *   Select the checkbox next to your policy.
    *   Click "Next".
4.  **Name Role:**
    *   **Role name:** Give your role a descriptive name (e.g., `LambdaS3toSNSRole`).
    *   Review the settings and click "Create role".

## 3. Create the Lambda Function

1.  **Navigate to Lambda:** Go to the AWS Lambda dashboard.
2.  **Create Function:**
    *   Click "Create function".
    *   Select "Author from scratch".
    *   **Function name:** Give your function a name (e.g., `s3FileNotificationToSNS`).
    *   **Runtime:** Select "Python 3.9" (or a newer Python version as available and compatible).
    *   **Architecture:** Choose your preferred architecture (e.g., `x86_64`).
    *   **Permissions:**
        *   Expand "Change default execution role".
        *   Select "Use an existing role".
        *   Choose the IAM role you created in Step 2 (e.g., `LambdaS3toSNSRole`).
    *   Click "Create function".
3.  **Configure Function Code:**
    *   In the "Code source" section:
        *   Open the `s3_to_sns_lambda.py` file.
        *   Copy its content.
        *   Paste the code into the `lambda_function.py` editor in the AWS console, replacing the default boilerplate code.
    *   Click "Deploy" to save your code.
4.  **Add Environment Variable:**
    *   Go to the "Configuration" tab, then "Environment variables".
    *   Click "Edit".
    *   Click "Add environment variable".
        *   **Key:** `SNS_TOPIC_ARN`
        *   **Value:** Paste the **SNS Topic ARN** you copied in Step 1.
    *   Click "Save".
5.  **Adjust Basic Settings (Optional but Recommended):**
    *   Go to the "Configuration" tab, then "General configuration".
    *   Click "Edit".
    *   **Memory:** Adjust as needed. For this function, 128 MB is likely sufficient.
    *   **Timeout:** Set an appropriate timeout (e.g., 10-30 seconds). The default of 3 seconds might be too short if there are network latencies.
    *   Click "Save".

## 4. Configure S3 Bucket Trigger

1.  **Navigate to S3:** Go to the S3 dashboard.
2.  **Select Bucket:** Click on the name of the S3 bucket to which you want to add the trigger.
3.  **Configure Event Notifications:**
    *   Go to the "Properties" tab.
    *   Scroll down to "Event notifications".
    *   Click "Create event notification".
    *   **Event name:** Give it a descriptive name (e.g., `LambdaTriggerOnFileUpload`).
    *   **Prefix (Optional):** If you want the Lambda to trigger only for files in a specific folder, enter the folder name here (e.g., `uploads/`).
    *   **Suffix (Optional):** If you want the Lambda to trigger only for specific file types, enter the suffix (e.g., `.jpg`).
    *   **Event types:** Select "All object create events" (or specifically `PUT`, `POST`, `CompleteMultipartUpload` if you prefer more granularity).
    *   **Destination:**
        *   Choose "Lambda function".
        *   **Lambda function:** Select the Lambda function you created in Step 3 (e.g., `s3FileNotificationToSNS`).
    *   Click "Save changes".
    *   AWS might add the necessary permissions to the Lambda function to be invoked by S3. If not, you might need to add a resource-based policy to the Lambda function manually, but usually S3 handles this.

## 5. Test

1.  **Upload a file:** Upload a new file to the S3 bucket (and into the specified prefix/suffix if you configured them).
2.  **Check Email:** You should receive an email notification at the address you subscribed to the SNS topic.
3.  **Check Lambda Logs (if troubleshooting):**
    *   Go to the Lambda function in the AWS console.
    *   Go to the "Monitor" tab.
    *   Click "View logs in CloudWatch". This will take you to the CloudWatch Log Group for your Lambda function.

---

You have now configured an AWS Lambda function to send email notifications via SNS when new files are uploaded to your S3 bucket. Remember to keep your IAM policies as restrictive as possible by specifying ARNs where applicable.
