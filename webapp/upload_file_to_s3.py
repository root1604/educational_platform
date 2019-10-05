import boto3

def upload_file_to_s3(file, bucket_name):
    # Let's use Amazon S3
    s3 = boto3.resource('s3')
    # Print out bucket names
    bucket_found = False
    for bucket in s3.buckets.all():
        if bucket.name == bucket_name:
            bucket_to_upload = bucket.name 
            bucket_found = True
    if bucket_found == False:    
        return 'Bucket not found' 
    s3 = boto3.client('s3')        
    try:
        s3.upload_fileobj(
            file,
            bucket_to_upload,
            file.filename,
            ExtraArgs={
                "ContentType": file.content_type
            }
        )
        s3 = boto3.session.Session()
        region = s3.region_name
        url = 'https://' + bucket_to_upload + '.s3.' + region + '.amazonaws.com/' + file.filename
        return url                                         
    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e