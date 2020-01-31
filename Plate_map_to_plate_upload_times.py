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



records_folder = input(r'Enter the folder path of the 2019 PLATE RECORDS folder: ')

df_plate_record_created = pd.DataFrame()
for foldername, subfolders, filenames in os.walk(records_folder):
    for file in filenames:
        plate_barcode = file[0:10].lower()

        record_ctime = os.path.getctime(foldername + '\\' + file)

        record_ctime = datetime.datetime.fromtimestamp(record_ctime)

        df = pd.DataFrame({'plate_barcode': [plate_barcode], 'time_created': [record_ctime]})
        df_plate_record_created = df_plate_record_created.append(df)



records_folder = input(r'Enter the folder path of the 2020 PLATE RECORDS folder: ')

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


df_final_posonly = df_final[(df_final['slow_cycle_time'] >= datetime.timedelta(days=0))]
print('Cycle time stats: \n', df_final_posonly['slow_cycle_time'].describe(percentiles=[.25, .5, .75, 0.95]))


pd.to_datetime(df_final['earliest_record'])


# cycle_time_months = []


# months2019 = [1,2,3,4,5,6,7,8,9,10,11,12]
# for m in months2019:
#     data_month = df_final_posonly[(df_final['earliest_record'].dt.month == m) &
#                                   (df_final_posonly['earliest_record'].dt.year == 2019)]
#     cycle_time_months.append(data_month['slow_cycle_time'].dt.days)
#
#
# months2020 = [1]
#
# for m in months2020:
#     data_month = df_final_posonly[(df_final_posonly['earliest_record'].dt.month == m) &
#                                   (df_final_posonly['earliest_record'].dt.year == 2020)]
#     cycle_time_months.append(data_month['slow_cycle_time'].dt.days)

cycle_time_weeks = []
labels_weeks = []
for week in range(1,53):
    data_week = df_final_posonly[(df_final_posonly['earliest_record'].dt.week == week) &
                                   (df_final_posonly['earliest_record'].dt.year == 2019)]
    cycle_time_weeks.append(data_week['slow_cycle_time'].dt.days)
    labels_weeks.append(str(week))

for week in range(1,5):
    data_week = df_final_posonly[(df_final_posonly['earliest_record'].dt.week == week) &
                                   (df_final_posonly['earliest_record'].dt.year == 2020)]
    cycle_time_weeks.append(data_week['slow_cycle_time'].dt.days)
    labels_weeks.append(str(week))


# labels = ['Jan 19', 'Feb 19', 'Mar 19', 'Apr 19', 'May 19', 'Jun 19', 'Jul 19', 'Aug 19', 'Sept 19', 'Oct 19',
#           'Nov 19', 'Dec 19', 'Jan 20']

# plt.boxplot(cycle_time_months, labels=labels)
plt.boxplot(cycle_time_weeks, labels=labels_weeks)
#plt.xlabel("Month when earliest record for plate created")
plt.xlabel("Week when earliest record for plate was created")
plt.ylabel("Earliest record to latest upload for each plate (Days)")
#plt.title("Boxplot for Monthly Cycle Times")
plt.title("Boxplot for Weekly Cycle Times 2019 and 2020")

plt.show()

#os.chdir(input(r'Please enter the path of the folder where you wish to save your excel file of the times plate records were created: '))
#excel_filename = input(r'Please enter the name of your excel file: ')
#excel_filename = excel_filename + '.xlsx'
#writer = pd.ExcelWriter(excel_filename, engine='openpyxl')
#df_final.to_excel(writer, header=True, index=True)
#writer.save()
#writer.close()
