import boto3
import os
import time
import os.path
import shutil

s3_resource = boto3.resource('s3')
s3_client=boto3.client('s3')
bucket_name = 'beft-mweb-out'

# these variables are empty and will be assigned values when used in the dowload_files() method
# afternoon1_file_object and afternoon2_file_object point to the files in the two sub directories
# s3_client.list_objects(Bucket='beft-mweb')['Contents'] returns an array of dictionaries
afternoon1_file_object = ''
afternoon2_file_object = ''

# these variables are empty and will be assigned values when used in the dowload_files() method
# determine the file names from the object
afternoon1_file_name = ''
afternoon2_file_name = ''

# specifies where on the local machine the files need to be downloaded to
download_path = 'C:/SBSA_HOST_TO_HOST/SBSA_OUT/'

# download_files_from_dir() uses the download_fileobj method of s3_client to download a file from s3
# download_fileobj expects the bucket, object and download destination
def download_files_from_dir(bucket, path, file):
    s3_client.download_file(bucket, path, file)
    with open(file, 'wb') as f:
        s3_client.download_fileobj(bucket, path, f)

def dowload_files():
    # afternoon1_file_count and afternoon2_file_count determine the presence of files in either
    # Afternoon1 or Afternoon2 directories
    afternoon1_file_count = len(s3_client.list_objects(Bucket= bucket_name, Prefix= 'Afternoon1/')['Contents'])
    afternoon2_file_count = len(s3_client.list_objects(Bucket= bucket_name, Prefix= 'Afternoon2/')['Contents'])
    # this block runs when there are files in both directories
    if afternoon1_file_count == 2 and afternoon2_file_count == 2:
        afternoon1_file_object = s3_client.list_objects(Bucket= bucket_name)['Contents'][1]['Key']
        afternoon2_file_object = s3_client.list_objects(Bucket= bucket_name)['Contents'][3]['Key']
        afternoon1_file_name = afternoon1_file_object.split('/')[1]
        afternoon2_file_name = afternoon2_file_object.split('/')[1]
        download_files_from_dir(bucket_name, afternoon1_file_object, download_path + afternoon1_file_name)
        # This while loop will run till the file downloaded from Afternoon1 has been deleted before allowing the file in Afternoon2 to be downloaded
        while os.path.isfile(download_path + afternoon1_file_name):
            time.sleep(30)
        download_files_from_dir(bucket_name, afternoon2_file_object, download_path + afternoon2_file_name)
        # files deleted from s3 once downloaded
        s3_client.delete_object(Bucket='beft-mweb-out', Key=afternoon2_file_object)
        s3_client.delete_object(Bucket='beft-mweb-out', Key=afternoon1_file_object)
    # this block runs if only Afternoon2 contains a file
    elif afternoon1_file_count == 1 and afternoon2_file_count == 2:
        afternoon2_file_object = s3_client.list_objects(Bucket= bucket_name)['Contents'][2]['Key']
        afternoon2_file_name = afternoon2_file_object.split('/')[1]
        download_files_from_dir(bucket_name, afternoon2_file_object, download_path + afternoon2_file_name)
        s3_client.delete_object(Bucket='beft-mweb-out', Key=afternoon2_file_object)
    # this block runs if only Afternoon1 contains a file
    elif afternoon1_file_count == 2 and afternoon2_file_count == 1:
        afternoon1_file_object = s3_client.list_objects(Bucket= bucket_name)['Contents'][1]['Key']
        afternoon1_file_name = afternoon1_file_object.split('/')[1]
        download_files_from_dir(bucket_name, afternoon1_file_object, download_path + afternoon1_file_name)
        s3_client.delete_object(Bucket='beft-mweb-out', Key=afternoon1_file_object)

dowload_files()
