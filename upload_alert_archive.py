import boto3
import os
import time
import os.path
import shutil
from datetime import date
import datetime
from archiving import archive_files
from send_email import send_email_notification

s3 = boto3.resource('s3')
dt = datetime.datetime.today()

# Buckets that files will be uploaded to
beft_afternoon_int = 'beft-afternoon-int'
beft_morning_final = 'beft-morning-final'
beft_morning_unpd = 'beft-morning-unpd'

# Directories that files will be uploaded from
int_aud_rep = 'C:/SBSA_HOST_TO_HOST/SBSA_IN/Production/SSVS/Int_Aud_Rep/'
fin_aud_rep = 'C:/SBSA_HOST_TO_HOST/SBSA_IN/Production/SSVS/Fin_Aud_Rep/'
unpd_data_rep = 'C:/SBSA_HOST_TO_HOST/SBSA_IN/Production/SSVS/Unpd_Data_Rep/'
#Archive Directories
int_aud_rep_archive = 'C:/SBSA_HOST_TO_HOST/SBSA_IN/Production/SSVS/Archive/Int_Aud_Rep/'
fin_aud_rep_archive = 'C:/SBSA_HOST_TO_HOST/SBSA_IN/Production/SSVS/Archive/Fin_Aud_Rep/'
unpd_date_rep_archive = 'C:/SBSA_HOST_TO_HOST/SBSA_IN/Production/SSVS/Archive/Unpd_Data_Rep/'

def upload_files(directory,bucket,archive):
    list_of_files = os.listdir(directory)
    if len(list_of_files) > 0:
        for file in list_of_files:
            s3.Bucket(bucket).upload_file(directory + file, file)
            archive_files(directory,archive)
            send_email_notification("Please look in the " + bucket + " bucket for todays files", 'Files uploaded to ' + bucket + ' for ' + str(datetime.date.today()) )

upload_files(int_aud_rep, beft_afternoon_int, int_aud_rep_archive)
upload_files(fin_aud_rep, beft_morning_final, fin_aud_rep_archive)
upload_files(unpd_data_rep, beft_morning_unpd, unpd_date_rep_archive)
