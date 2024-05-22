yc-aws-wrapper
=
### About:
A little sugar for working with Yandex cloud services. May also be compatible with other AWS clones.   
The wrapper is written for your own needs and primarily for working with Yandex Cloud, ready for criticism and suggestions.

To run tests, in addition to the necessary environment variables, you need S3_BUCKET the location of your test bucket

#### ENV:  
- **REQUIRED**
  >AWS_REGION: region  
  AWS_ACCESS_KEY_ID: key id  
  AWS_SECRET_ACCESS_KEY: secret from key id  
- **SITUATIONAL**:
  > [SERVICE]_ENDPOINT_URL: endpoint for the service, example for yandex sqs: `SQS_ENDPOINT_URL=https://message-queue.api.cloud.yandex.net`    
- **ADDITIONAL**:
  - ***Kinesis***:  
    >KINESIS_FOLDER:   
    KINESIS_DATABASE:  
    KINESIS_STREAM_NAME:  
