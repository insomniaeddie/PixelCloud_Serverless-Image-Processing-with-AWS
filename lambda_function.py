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
