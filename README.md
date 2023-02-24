# Serverless Image Processing with AWS Lambda and Amazon S3



Table of Contents:

- [Project Description](#project-description)
- [Prerequisites](#prerequisites)
- [Steps](#steps)
  * [1. Create an S3 bucket for the original images.](#1-create-an-s3-bucket-for-the-original-images)
  * [2. Create an S3 bucket for the processed images.](#2-create-an-s3-bucket-for-the-processed-images)
  * [3. Create an IAM role for the Lambda function.](#3-create-an-iam-role-for-the-lambda-function)
  * [4. Create a Lambda function in Python.](#4-create-a-lambda-function-in-python)
  * [5. Use the Pillow library to resize and optimize images.](#5-use-the-pillow-library-to-resize-and-optimize-images)
  * [6. Set up S3 events to trigger the Lambda function](#6-set-up-s3-events-to-trigger-the-lambda-function)
  * [7. Test the Image Processing Function](#7-test-the-image-processing-function)
  * [8. Monitor the Lambda function](#8-monitor-the-lambda-function)
- [Conclusion](#conclusion)





### Project Description

This project will guide you on how to use AWS Lambda and Amazon S3 to create a serverless image processing service that will automatically optimize and resize images. The images are uploaded to an S3 bucket and the Lambda function will automatically trigger to process the image. The processed image will be stored in another S3 bucket. This project will help you to create an image processing pipeline that can automatically process images as soon as they are uploaded to the source bucket.



### Prerequisites

- Basic understanding of AWS Lambda and Amazon S3

- AWS CLI installed on your local machine

- An AWS account

  

### Steps

1. Create an S3 bucket for the original images.
2. Create an S3 bucket for the processed images.
3. Create an IAM role for the Lambda function.
4. Create a Lambda function in Python.
5. Use the Pillow library to resize and optimize images.
6. Set up an S3 event to trigger the Lambda function.
7. Test the image processing pipeline by uploading an image to the source bucket.
8.  Monitor the Lambda function 



#### 1. Create an S3 bucket for the original images.

- Open the AWS S3 console.

- Click the "Create Bucket" button.

- Enter a unique name for your bucket and select a region.

- Leave the default settings and click "Create Bucket".

  ![1-create_S3buckets](https://user-images.githubusercontent.com/49099173/221090209-6587318e-8db2-4ff0-a8d6-320615ece2a7.PNG)


#### 2. Create an S3 bucket for the processed images.

- Follow the same steps as for the original images bucket.

  

#### 3. Create an IAM role for the Lambda function.

- Open the IAM console.

- Click on "Roles" and then "Create role".

- Choose Lambda as the service that will use this role.

- Attach the "AmazonS3FullAccess" policy to this role.

- Name your role and click "Create Role".

  ![2b-IAM_role_Lambda](https://user-images.githubusercontent.com/49099173/221090254-3e27f714-713a-4123-b0ac-43a290b7b2e8.PNG style="zoom: 50%;")


#### 4. Create a Lambda function in Python.

- Open the AWS Lambda console.

- Click the "Create Function" button.

- Choose "Author from scratch" and give your function a name.

- Choose "Python 3.8" as the runtime and select the IAM role you created in step 3.

- Click "Create Function".

  

#### 5. Use the Pillow library to resize and optimize images.

- Add the following code to your Lambda function:

  ```python
  import os
  import boto3
  from PIL import Image
  import io
  
  
  def lambda_handler(event, context):
      s3 = boto3.client("s3")
      src_bucket = event["Records"][0]["s3"]["bucket"]["name"]
      src_key = event["Records"][0]["s3"]["object"]["key"]
      dst_bucket = os.environ['DEST_BUCKET_NAME']
      dst_key = src_key
  
      try:
          # download image from s3
          image_byte_array = s3.get_object(
              Bucket=src_bucket, Key=src_key)['Body'].read()
          
          # resize and optimize image
          image_name = os.path.splitext(os.path.basename(src_key))[0]
          image_size = None
          
          # check if image name contains size information
          if '_' in image_name:
              parts = image_name.split('_')
              if len(parts) == 2:
                  try:
                      width, height = map(int, parts[1].split('x'))
                      image_size = (width, height)
                  except ValueError:
                      pass
  
          image = Image.open(io.BytesIO(image_byte_array))
          image = image.convert("RGB")
  
          if image_size is not None:
              image = image.resize(image_size)
  
          buffer = io.BytesIO()
          image.save(buffer, "JPEG", optimize=True, quality=85)
          buffer.seek(0)  
         
  
          # upload image to s3
          s3.upload_fileobj(Fileobj=buffer, Bucket=dst_bucket, Key=dst_key)
  
          # set content type to image/jpeg
          s3.put_object(Bucket=dst_bucket, Key=dst_key,
                        Body=buffer.getvalue(), ContentType='image/jpeg')
  
      except Exception as e:
          print(e)
          raise e
  
  
  ```

This Lambda function downloads an image from an S3 bucket, resizes and optimizes it, and then uploads the processed image to another S3 bucket. Note that you will need to set the `DEST_BUCKET_NAME` environment variable for this code to work.

You can set the environment variable in the AWS Lambda function configuration. In the AWS Lambda console, go to the "Configuration" tab of the Lambda function, scroll down to the "Environment variables" section, and add a new environment variable with the key "DEST_BUCKET_NAME" and the value set to the name of your destination S3 bucket.

<img src="https://user-images.githubusercontent.com/49099173/221090289-b67c6260-8a9c-4f50-b440-6091098ce5d1.PNG" style="zoom: 38%;"/>


####  6. Set up S3 events to trigger the Lambda function

 Now, set up S3 events to trigger the Lambda function when an image is uploaded to the S3 bucket.

To trigger the Lambda function when an image is uploaded to the S3 bucket, you need to set up S3 events. Here are the steps to do so:

1. Go to the AWS Management Console and navigate to the S3 service.
2. Select the S3 bucket where you want to trigger the Lambda function.
3. Click on the "Properties" tab.
4. Scroll down to the "Event notifications" section and click on the "Create event notification" button.
5. In the "Create Event" dialog, select the "All object create events" option under "Event types".
6. Under "Destination", select "Lambda Function".
7. Choose the Lambda function you created to process the images.
8. Click on the "Save" button to create the S3 event.

Now, whenever an image is uploaded to the S3 bucket, the Lambda function will be triggered to process the image.



#### 7. Test the Image Processing Function 

You can now test the image processing function using the AWS Lambda console, AWS CLI, or your own custom application.



#### 8. Monitor the Lambda function 

You can monitor the Lambda function and check its status using Amazon CloudWatch. 



When you're done testing and using the image processing function, make sure to clean up the resources to avoid any additional charges.



### Conclusion 

In conclusion, the Serverless Image Processing with AWS Lambda and Amazon S3 project is a great introduction to serverless computing and AWS Lambda functions. The project provides a hands-on experience in developing an end-to-end serverless solution for image processing using AWS services.

The project requires some prior knowledge of programming and AWS services, but the step-by-step guide and resources provided in the documentation make it accessible for beginners. The project is also customizable, allowing for modifications and extensions based on specific needs.



