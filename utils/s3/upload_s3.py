import boto3

def upload(aws_s3_bucket_name, aws_region, aws_access_key, aws_secret_key, local_file, s3_file_name):
    try:
        s3_client = boto3.client(
            service_name= 's3',
            region_name=aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key = aws_secret_key
        )

        response = s3_client.upload_file(local_file, aws_s3_bucket_name, s3_file_name)

        print(f'upload_log_to_aws response: {response}')
    except Exception as ex:
        print(ex)

def put_object(aws_s3_bucket_name, aws_region, aws_access_key, aws_secret_key, local_file, s3_file_name):
    try:
        s3_client = boto3.client(
            service_name= 's3',
            region_name=aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key = aws_secret_key
        )

        response = s3_client.put_object(Bucket = aws_s3_bucket_name, Key=s3_file_name, Body = local_file)

        return response
    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    put_object()