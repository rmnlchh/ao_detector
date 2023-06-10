import io
from datetime import datetime

import boto3
from botocore.exceptions import NoCredentialsError

from utils import data_bucket, test_bucket

# Set up the AWS SDK client
rekognition_client = boto3.client('rekognition',
                                  aws_access_key_id='AK',
                                  aws_secret_access_key='SK',
                                  region_name='us-east-1')

s3_client = boto3.client('s3',
                         aws_access_key_id='AK',
                         aws_secret_access_key='SK',
                         region_name='us-east-1')

s3_resource = boto3.resource('s3',
                             aws_access_key_id='AK',
                             aws_secret_access_key='SK',
                             region_name='us-east-1')


def analyze_image(user_id, photo_file):
    s3_bucket_name = 'airborne-object-detection-test'

    # create a file path and name
    file_path = f'{user_id}/{datetime.now().strftime("%Y%m%d")}'
    filename = f'{file_path}/{photo_file.file_id}.jpg'

    # Download photo into byte stream
    photo_data = io.BytesIO(photo_file.download_as_bytearray())

    # upload the photo to S3
    s3_client.upload_fileobj(photo_data, s3_bucket_name, filename)

    project_version_arn = 'arn:aws:rekognition:us-east-1:673007394197:project/ao_detection/version/ao_detection.2023-05-28T16.05.46/1685282746786'

    # Test the model on a new image
    test_image = {'S3Object': {'Bucket': s3_bucket_name, 'Name': filename}}
    response = rekognition_client.detect_custom_labels(ProjectVersionArn=project_version_arn, Image=test_image,
                                                       MinConfidence=50)
    if len(response['CustomLabels']) == 0:
        return None
    else:
        highest_confidence_label = max(response['CustomLabels'], key=lambda x: x['Confidence'])
        return highest_confidence_label


def add_to_dataset(user_id, object_type):
    # Get the S3.Object summaries for the highest alphabetical folder
    latest_file = get_latest_file(test_bucket, f'{user_id}/')

    try:
        # Copy the latest file to the target bucket
        copy_source = {
            'Bucket': test_bucket,
            'Key': latest_file
        }

        # Get the filename from the source key
        filename = latest_file.split('/')[-1]

        # Build the target key
        target_key = f'{object_type}/{filename}'

        s3_client.copy(copy_source, data_bucket, target_key)

        print(f"File {latest_file} copied to {data_bucket}.")
    except NoCredentialsError:
        print("Credentials not available")


def get_latest_file(bucket_name, prefix):
    my_bucket = s3_resource.Bucket(bucket_name)
    prefixes = [obj.key for obj in my_bucket.objects.filter(Prefix=f'{prefix}').all()]
    return max(prefixes)


def read_obj_to_bytes(bucket, prefix):
    # Create a file object using the bucket and object key.
    file_obj = s3_client.get_object(Bucket=bucket, Key=prefix)

    # open the file object and read it into the variable file_data.
    file_data = file_obj['Body'].read()

    # convert binary file data into bytes array for telegram
    return io.BytesIO(file_data)
