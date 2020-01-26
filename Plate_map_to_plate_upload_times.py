"""
Data is harvested from the genotyping team drive to determine how long a plate takes to from having a record made to
appearing in the database uploads folder. Returns an Excel spreadsheet with columns: plate_id, earliest_record,
latest_record, earliest_upload, latest_upload.
Created by TABS
version 2020.01.26

"""

import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt



records_folder = input(r'Enter the folder path of a plate records folder: ')

df_plate_record_created = pd.DataFrame()
for foldername, subfolders, filenames in os.walk(records_folder):
    for file in filenames:
        plate_barcode = file[0:10].lower()

        record_ctime = os.path.getctime(foldername + '\\' + file)

        record_ctime = datetime.datetime.fromtimestamp(record_ctime)

        df = pd.DataFrame({'plate_barcode': [plate_barcode], 'time_created': [record_ctime]})
        df_plate_record_created = df_plate_record_created.append(df)




df_earliest_record = df_plate_record_created.sort_values(by='time_created').drop_duplicates('plate_barcode', keep='first')
df_earliest_record.rename(columns={'time_created': 'earliest_record'}, inplace=True)


df_latest_record = df_plate_record_created.sort_values(by='time_created').drop_duplicates('plate_barcode', keep='last')
df_latest_record.rename(columns={'time_created': 'latest_record'}, inplace=True)


df_plate_records = df_earliest_record.merge(df_latest_record)




uploads_folder = input(r'Enter the folder path of your 2019 database uploads folder: ')

df_plate_upload_created = pd.DataFrame()
for foldername, subfolders, filenames in os.walk(uploads_folder):
    for file in filenames:
        for plate in df_plate_record_created['plate_barcode']:
            if plate[5:] in file:
                plate_barcode = plate


                upload_ctime = os.path.getctime(foldername + '\\' + file)

                upload_ctime = datetime.datetime.fromtimestamp(upload_ctime)

                df = pd.DataFrame({'plate_barcode': [plate_barcode], 'time_created': [upload_ctime]})
                df_plate_upload_created = df_plate_upload_created.append(df)

            else:
                continue


uploads_folder = input(r'Enter the folder path of your 2020 database uploads folder: ')

for foldername, subfolders, filenames in os.walk(uploads_folder):
    for file in filenames:
        for plate in df_plate_record_created['plate_barcode']:
            if plate[5:] in file:
                plate_barcode = plate


                upload_ctime = os.path.getctime(foldername + '\\' + file)

                upload_ctime = datetime.datetime.fromtimestamp(upload_ctime)

                df = pd.DataFrame({'plate_barcode': [plate_barcode], 'time_created': [upload_ctime]})
                df_plate_upload_created = df_plate_upload_created.append(df)

            else:
                continue


df_earliest_upload = df_plate_upload_created.sort_values(by='time_created').drop_duplicates('plate_barcode', keep='first')
df_earliest_upload.rename(columns={'time_created': 'earliest_upload'}, inplace=True)

df_latest_upload = df_plate_upload_created.sort_values(by='time_created').drop_duplicates('plate_barcode', keep='last')
df_latest_upload.rename(columns={'time_created': 'latest_upload'}, inplace=True)

df_plate_uploads = df_earliest_upload.merge(df_latest_upload)



df_final = df_plate_records.merge(df_plate_uploads)




df_final['slow_cycle_time'] = df_final['latest_upload'].subtract(df_final['earliest_record'])

df_final['fast_cycle_time'] = df_final['earliest_upload'].subtract(df_final['earliest_record'])


df_slow_posonly = df_final[(df_final['slow_cycle_time'] >= datetime.timedelta(days=0))]
print('Slow cycle time stats: \n', df_slow_posonly['slow_cycle_time'].describe(percentiles=[.25, .5, .75, 0.95]))

df_fast_posonly = df_final[(df_final['fast_cycle_time'] >= datetime.timedelta(days=0))]
print('\n\nFast cycle time stats: \n', df_fast_posonly['fast_cycle_time'].describe(percentiles=[.25, .5, .75, 0.95]))

pd.to_datetime(df_final['earliest_record'])

months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
cycle_time_months = []

for m in months:
    data_month = df_final[(df_final['earliest_record'].dt.month == m) & (df_final['earliest_record'].dt.year == 2019)]
    cycle_time_months.append(data_month['slow_cycle_time'].dt.days)

labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
plt.boxplot(cycle_time_months, labels=labels)
plt.xlabel("Month when earliest record for plate created")
plt.ylabel("Earliest record to latest upload (Days)")
plt.title("Monthly Cycle Times for 2019 boxplot")

plt.show()



