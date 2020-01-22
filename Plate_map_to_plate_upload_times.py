"""
Data is harvested from the genotyping team drive to determine how long a plate takes to from having a record made to
appearing in the database uploads folder. Returns an Excel spreadsheet with columns: plate_id, earliest_record,
latest_record, earliest_upload, latest_upload.
Created by TABS
version 2020.01.17

"""

import os
import datetime
import pandas as pd


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

print(df_plate_records)

uploads_folder = input(r'Enter the folder path of your database uploads folder: ')

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



df_earliest_upload = df_plate_upload_created.sort_values(by='time_created').drop_duplicates('plate_barcode', keep='first')
df_earliest_upload.rename(columns={'time_created': 'earliest_upload'}, inplace=True)

df_latest_upload = df_plate_upload_created.sort_values(by='time_created').drop_duplicates('plate_barcode', keep='last')
df_latest_upload.rename(columns={'time_created': 'latest_upload'}, inplace=True)

df_plate_uploads = df_earliest_upload.merge(df_latest_upload)


df_final = df_plate_records.merge(df_plate_uploads)


os.chdir(input(r'Please enter the path of the folder where you wish to save your excel file of the times plate records were created: '))
excel_filename = input(r'Please enter the name of your excel file: ')
excel_filename = excel_filename + '.xlsx'
writer = pd.ExcelWriter(excel_filename, engine='openpyxl')
df_final.to_excel(writer, header=True, index=True)
writer.save()
writer.close()