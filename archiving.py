import os
import shutil
import time
from datetime import date
import datetime
from send_email import send_email_notification

# instantiating date time object
dt = datetime.datetime.today()



#returns name of month and month_year
def month_year():
    # assigning names of months to a dictionary to be used by month_year
    month_names = {
      1 : "January", 2 : "February", 3 : "March", 4 : "April", 5 : "May", 6 : "June", 7 : "July",
      8 : "August", 9 : "September", 10 : "October", 11 : "November", 12 : "December"}
    return month_names[dt.month] + str(dt.year)

def archive_files(source,archive_root):
    # lists files in the source directory
    listfiles = os.listdir(source)
    # checks if the directory for the current month exists, if not, it creates it
    # directory name is the month and year concatenated, eg: September2020 as per month_year()
    if not os.path.isdir(archive_root + month_year()):
        os.mkdir(archive_root + month_year())
    for file_name in listfiles:
        archive_destination = archive_root + month_year() + '/'
        shutil.move(source + file_name, archive_destination + file_name)
