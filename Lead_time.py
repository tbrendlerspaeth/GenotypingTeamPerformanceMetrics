"""
Script that generates lead time data for plates processed by a genoptying team.
created by TABS
version 2020.02.01

"""

import os
import pandas as pd
import datetime


plates_received = 'Plates received 1 Sept 2019 to 29 Jan 2020 db report.csv'

df_received = pd.read_csv(plates_received)
df_received = df_received[['Plate Barcode', 'Assignment Date']]
df_received.rename(columns={'Plate Barcode': 'plate', 'Assignment Date': 'received'}, inplace=True)


uploads_folder = input(r'Enter the folder path of your 2019 database uploads folder: ')

df_plate_upload_created = pd.DataFrame()
for foldername, subfolders, filenames in os.walk(uploads_folder):
    for file in filenames:
        for plate in df_received['plate']:
            if plate[5:] in file:

                upload_ctime = os.path.getctime(foldername + '\\' + file)

                upload_ctime = datetime.datetime.fromtimestamp(upload_ctime)

                df = pd.DataFrame({'plate': [plate], 'time uploaded': [upload_ctime]})
                df_plate_upload_created = df_plate_upload_created.append(df)

            else:
                continue


uploads_folder = input(r'Enter the folder path of your 2020 database uploads folder: ')

for foldername, subfolders, filenames in os.walk(uploads_folder):
    for file in filenames:
        for plate in df_received['plate']:
            if plate[5:] in file:

                upload_ctime = os.path.getctime(foldername + '\\' + file)

                upload_ctime = datetime.datetime.fromtimestamp(upload_ctime)

                df = pd.DataFrame({'plate': [plate], 'time uploaded': [upload_ctime]})
                df_plate_upload_created = df_plate_upload_created.append(df)

            else:
                continue




df_latest_upload = df_plate_upload_created.sort_values(by='time uploaded').drop_duplicates('plate', keep='last')
df_latest_upload.rename(columns={'time uploaded': 'latest upload'}, inplace=True)



df_final = df_received.merge(df_latest_upload)


df_final['lead time'] = df_final['latest upload'].subtract(df_final['received'])



with pd.ExcelWriter('PBC Template.xlsx', mode='w') as writer:
    df_final.to_excel(writer, sheet_name='PBC', columns=['received', 'latest upload'], startrow=1,
                         startcol=0, index=False)



os.startfile('PBC Template.xlsx')