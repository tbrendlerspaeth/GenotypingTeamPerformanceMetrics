import os
import datetime
import pandas as pd


records_folder = input(r'Enter the folder path of a plate records folder: ')

plate_record_created = pd.DataFrame()
for foldername, subfolders, filenames in os.walk(records_folder):
    for file in filenames:
        plate_id = file[0:10]
        # print(plate_id)

        record_ctime = os.path.getctime(foldername + '\\' + file)
        record_ctime = datetime.datetime.fromtimestamp(record_ctime).date()
        # print(record_ctime)

        df = pd.DataFrame({'plate_id': [plate_id], 'time_created': [record_ctime]})
        plate_record_created = plate_record_created.append(df)

# print(plate_record_created)

os.chdir(input(r'Please enter the path of the folder where you wish to save your excel file of the times plate records were created: '))
excel_filename = input(r'Please enter the name of your excel file: ')
excel_filename = excel_filename + '.xlsx'
writer = pd.ExcelWriter(excel_filename, engine='openpyxl')
plate_record_created.to_excel(writer, header=True, index=True)
writer.save()
writer.close()