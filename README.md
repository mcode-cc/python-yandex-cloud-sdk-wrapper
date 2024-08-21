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
  - ***SQS***:   
    >SQS_TUBE_[Method_Name]: Contains the name of the queue to be accessed via a method.  
      Example: SQS_TUBE_FOO=sqs-aws-wrapper | sqs.foo.send(*args, **kwargs)  
  - ***S3***:   
    >S3_BUCKET_[Method_Name]: Contains the name of the bucket to be accessed via a method.  
      Example: S3_BUCKET_FOO=bucket-aws-wrapper | s3.foo.send(*args, **kwargs) 
  - ***SESV2***:   
    >SESV2_MAILBOX_[Method_Name]: Contains the name of the mailbox to be accessed via a method.  
      Example: SESV2_MAILBOX_FOO=mail@aws-wrapper.net | sesv2.foo.send(*args, **kwargs)   
  - ***Kinesis***:  
    >KINESIS_FOLDER:   
    KINESIS_DATABASE:  
    KINESIS_STREAM_NAME:  

#### Example:
Let's send a message to three queues, one of which is not declared in the environment variables, as a result we will get dictionaries symbolizing a successful result for "foo" and "bar", as well as none, indicating that nothing was sent, example code_1      
You can also send a message to all queues using a loop, but first you need to force load all environment variables, example code_2
envs:   
> AWS_REGION=ru.central1   
> AWS_ACCESS_KEY_ID=<KEY_ID>  
> AWS_SECRET_ACCESS_KEY=<SECRET_KEY>  
> SQS_ENDPOINT_URL=`https://message-queue.api.cloud.yandex.net`  
> SQS_TUBE_FOO=foo-aws-wrapper
> SQS_TUBE_BAR=bar-aws-wrapper

code_1:
> import from yc_aws_wrapper.s3 import SQS   
>   
> sqs = SQS()   
> response = sqs.foo.send("Hellow World")   
> type(response) is dict   
> response = sqs.bar.send("Hellow World")   
> type(response) is dict   
> response = sqs.baz.send("Hellow World")   
> type(response) is None   

code_2:
> import from yc_aws_wrapper.s3 import SQS   
>   
> sqs = SQS()   
> sqs.load_all_clients()   
> for el in sqs:   
>   el.send("Hellow World")