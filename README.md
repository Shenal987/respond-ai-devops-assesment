# respond-ai-devops-assesment

## Deployment Steps

### 1. Initialize the project
```bash
sam init --architecture arm64
sam build
sam deploy --guided --profile {profile-name}
```
### 2. To deploy changes
```bash
sam deploy --profile {profile-name}
```
### 3. To delete stack
```bash
sam delete --stack-name s3-lambda-trigger --profile {profile-name}
```

### How to Test

 1. Create original/ and compressed/ folders inside relevant s3 bucket

 2. Open AWS S3 Console and upload a JSON file to original/test.json and this upload will automatically trigger the Lambda function

### Expected Result

JSON file is downloaded by Lambda and file is compressed into ZIP to compressed/test.json.zip and with tha original JSON file is deleted


### Estimated Cost
https://calculator.aws/#/estimate?id=657a12b82bc8cdba6303d435f53414b327f7df23

### Sugeestions
1. Use SQS Batch Processing to Reduce Lambda Requests
    Instead of triggering a Lambda for every S3 object upload, route events through Amazon SQS and process messages in batches.

2. Apply S3 Lifecycle Policies to Reduce Storage Cost
    Lifecycle rules to automatically move objects to cheaper storage classes.

3. Avoid Sending JSON Directly from S3 to Lambda
    Process data via API Gateway instead of direct S3.


### Current Architecture
Yes the solution is scalable but not cost efficent.

1. Serverless architecture 
    Lambda is scalable automatically and no server compute management.

2. Even driven
    Lambda trigger only when only file is uploaded. So no idle compute and only pay for usage.

3. VPC endpoint to S3
    Private network communication. Reduce network cost and security.


### Bottelneck and Concerns

1. 1,000,000 Lambda invocations/hour
    Increase cost and concurrency pressure will create slowe processing with potential throttling

2. S3 cost

3. Lambda execution memory and time
    Larger json file data to data/io and compressing required more cpu. Therefore fine tuning of resources must needed for faster throughput.