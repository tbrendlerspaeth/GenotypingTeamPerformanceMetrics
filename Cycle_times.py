"""
Data is harvested from the genotyping team drive to determine how long a plate takes to from having a record made to
appearing in the database uploads folder. Returns a boxplot with cycle times by week or month depending on what's
commented out at the time. Time period of data collected can be specified by user input regarding which folders data
is harvested from.
Created by TABS
version 2020.01.31

"""

print("Loading modules...")

import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np


print("\nSearching qPCR plate record files...")


# records_folder = input(r'Enter the folder path of the 2019 PLATE RECORDS folder: ')
records_folder = r'\\file01-s0\team121\Genotyping\qPCR 2019\PLATE RECORDS'
df_plate_record_created = pd.DataFrame()
for foldername, subfolders, filenames in os.walk(records_folder):
     for file in filenames:
         plate_barcode = file[0:10].lower()

         record_ctime = os.path.getctime(foldername + '\\' + file)

         record_ctime = datetime.datetime.fromtimestamp(record_ctime)

         df = pd.DataFrame({'plate_barcode': [plate_barcode], 'time_created': [record_ctime]})
         df_plate_record_created = df_plate_record_created.append(df)



# records_folder = input(r'Enter the folder path of the 2020 PLATE RECORDS folder: ')
records_folder = r'\\file01-s0\team121\Genotyping\qPCR 2020\PLATE RECORDS'
for foldername, subfolders, filenames in os.walk(records_folder):
     for file in filenames:
         plate_barcode = file[0:10].lower()

         record_ctime = os.path.getctime(foldername + '\\' + file)

         record_ctime = datetime.datetime.fromtimestamp(record_ctime)

         df = pd.DataFrame({'plate_barcode': [plate_barcode], 'time_created': [record_ctime]})
         df_plate_record_created = df_plate_record_created.append(df)



print("\nSearching E-gels plate record files...")


records_folder = r'\\file01-s0\team121\Genotyping\E-gels of genotyping\2019'
for foldername, subfolders, filenames in os.walk(records_folder):
    for file in filenames:
        plate_barcode = file[9:19].lower()

        record_ctime = os.path.getctime(foldername + '\\' + file)

        record_ctime = datetime.datetime.fromtimestamp(record_ctime)

        df = pd.DataFrame({'plate_barcode': [plate_barcode], 'time_created': [record_ctime]})
        df_plate_record_created = df_plate_record_created.append(df)



records_folder = r'\\file01-s0\team121\Genotyping\E-gels of genotyping\2020'
for foldername, subfolders, filenames in os.walk(records_folder):
    for file in filenames:
        plate_barcode = file[9:19].lower()

        record_ctime = os.path.getctime(foldername + '\\' + file)

        record_ctime = datetime.datetime.fromtimestamp(record_ctime)

        df = pd.DataFrame({'plate_barcode': [plate_barcode], 'time_created': [record_ctime]})
        df_plate_record_created = df_plate_record_created.append(df)



df_earliest_record = df_plate_record_created.sort_values(by='time_created').drop_duplicates('plate_barcode', keep='first')
df_earliest_record.rename(columns={'time_created': 'earliest_record'}, inplace=True)

df_latest_record = df_plate_record_created.sort_values(by='time_created').drop_duplicates('plate_barcode', keep='last')
df_latest_record.rename(columns={'time_created': 'latest_record'}, inplace=True)

df_plate_records = df_earliest_record.merge(df_latest_record)



print("\nInterrogating database entries files...")



# uploads_folder = input(r'Enter the folder path of your 2019 database uploads folder: ')
uploads_folder = r'\\file01-s0\team121\Genotyping\Database entries\2019'
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


print("\nAlmost there...")


# uploads_folder = input(r'Enter the folder path of your 2020 database uploads folder: ')
uploads_folder = r'\\file01-s0\team121\Genotyping\Database entries\2020'
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
df_final_posonly = df_final_posonly[(df_final_posonly['fast_cycle_time'] >= datetime.timedelta(days=0))]

# pd.to_datetime(df_final['earliest_record'])




df_sept_dec_19 = df_final_posonly[(df_final_posonly['earliest_record'].dt.month.isin((9,10,11,12))) &
                                   (df_final_posonly['earliest_record'].dt.year == 2019)]
print('\nCycle time stats for Sept - Dec 2019: \n', df_sept_dec_19['slow_cycle_time'].describe(percentiles=[.25, .5, .75, 0.95]))


df_2020 = df_final_posonly[df_final_posonly['earliest_record'].dt.year == 2020]
print('\nCycle time stats for 2020: \n', df_2020['slow_cycle_time'].describe(percentiles=[.25, .5, .75, 0.95]))





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

#cycle_time_weeks = []
#labels_weeks = []
#for week in range(36,53): # week 39 = start 2nd Sept 2019
#    data_week = df_final_posonly[(df_final_posonly['earliest_record'].dt.week == week) &
#                                   (df_final_posonly['earliest_record'].dt.year == 2019)]
#    cycle_time_weeks.append(data_week['slow_cycle_time'].dt.days)
#    labels_weeks.append(str(week))
#
#for week in range(1,12):
#    data_week = df_final_posonly[(df_final_posonly['earliest_record'].dt.week == week) &
#                                   (df_final_posonly['earliest_record'].dt.year == 2020)]
#    cycle_time_weeks.append(data_week['slow_cycle_time'].dt.days)
#    labels_weeks.append(str(week))


# labels = ['Jan 19', 'Feb 19', 'Mar 19', 'Apr 19', 'May 19', 'Jun 19', 'Jul 19', 'Aug 19', 'Sept 19', 'Oct 19',
#           'Nov 19', 'Dec 19', 'Jan 20']

# plt.boxplot(cycle_time_months, labels=labels)
# plt.boxplot(cycle_time_weeks, labels=labels_weeks)
#plt.xlabel("Month when earliest record for plate created")
# plt.xlabel("Week when earliest record for plate was created")
# plt.ylabel("Earliest record to latest upload for each plate (Days)")
#plt.title("Boxplot for Monthly Cycle Times")
# plt.title("Boxplot for Weekly Cycle Times 2019 and 2020")
#
# plt.show() # Should this be plotted by date of latest record instead? is the current boxplot misleading?



# plt.plot(df_final_posonly['earliest_record'], df_final_posonly['slow_cycle_time'].dt.days)

#mean_cycle_time = df_final_posonly['slow_cycle_time'].dt.days.mean()
#print('Mean cycle time:', mean_cycle_time)

#std_cycle_time = df_final_posonly['slow_cycle_time'].dt.days.std()
#print('Std cycle time:', std_cycle_time)

#ucl_cycle_time = mean_cycle_time + 2*std_cycle_time
#print('UCL cycle time:', ucl_cycle_time)

#plt.plot([df_final_posonly['earliest_record']], [ucl_cycle_time, ucl_cycle_time], color='red') # must specify range for line. need max and min eariest record coocoridnates
#plt.axvline(ucl_cycle_time, color='red')
#plt.hlines(ucl_cycle_time, colors='r')
# plt.axhline(y=ucl_cycle_time, color='r', linestyle='-')
# plt.show()


# Could I plot mean and median cycle times for all the weeks of interest?
#quantile = 0.75
#quantile_val = df_final_posonly['slow_cycle_time'].dt.days.quantile(q=quantile)
#print(quantile_val)
#df_flagged_plates_quantile = df_final_posonly[(df_final_posonly['slow_cycle_time'].dt.days > quantile_val) &
#                                     (df_final_posonly['earliest_record'].dt.year == 2020)]
#print("Plates with a cycle time above specified quantile (" + str(quantile) + "):")
#print(df_flagged_plates_quantile[['plate_barcode', 'slow_cycle_time']])




#df_flagged_plates_cutoff = df_final_posonly[(df_final_posonly['slow_cycle_time'].dt.days > 7) &
#                                     (df_final_posonly['earliest_record'].dt.year == 2020)]
#print("Plates with a cycle time of more than 7 days in 2020: ")
#print(df_flagged_plates_cutoff[['plate_barcode', 'slow_cycle_time']])

#os.chdir(input(r'Please enter the path of the folder where you wish to save your excel file of the times plate records were created: '))
#excel_filename = input(r'Please enter the name of your excel file: ')
#excel_filename = excel_filename + '.xlsx'
#writer = pd.ExcelWriter(excel_filename, engine='openpyxl')
#df_final.to_excel(writer, header=True, index=True)
#writer.save()
#writer.close()


# ROLLING STATISTICS
today = datetime.date.today()
from_date = datetime.date(2019, 9, 2)
to_date = today    
#pbc_data = df_final_posonly[df_final_posonly['earliest_record'].dt.year == 2020]
df_final_posonly.set_index('earliest_record', inplace=True)
pbc_data = df_final_posonly.loc[from_date:to_date]
# window = int(len(pbc_data)*0.1)
offset = '7D'
min_periods = 10
x = pbc_data.index
y = pbc_data['slow_cycle_time'].dt.days
plt.scatter(x, y, color='black', label='Plate', marker='o', s=15, facecolors='none', edgecolors='black', alpha=0.5)


# Create rolling statistics
pbc_cycle_times = pbc_data['slow_cycle_time'].dt.days
rolmean = pbc_cycle_times.rolling(window=offset, min_periods=min_periods).mean()
rolmedian = pbc_cycle_times.rolling(window=offset, min_periods=min_periods).median()
rolstd = pbc_cycle_times.rolling(window=offset, min_periods=min_periods).std()
rolucl = rolmean + 2 * rolstd

# Plot rolling statistics:

plt.plot(rolmean, color='green', label='Rolling Mean')
plt.plot(rolucl, color='red', label='Rolling Upper Control Limit (mean+2*std)')
plt.plot(rolmedian, color='blue', label='Rolling Median')
plt.xlabel("Date of earliest plate record", fontdict={'fontsize':14})
plt.ylabel("Plate cycle time (Days)", fontdict={'fontsize':14})
plt.grid(axis='y')
plt.legend(loc='best', fontsize=12, facecolor='white', framealpha=1)
y_max = y.max()
plt.yticks(np.arange(0, int(y_max + y_max*0.2), 10)) # this works better
plt.xticks(np.arange(from_date, to_date, datetime.timedelta(weeks=2)).astype(datetime.datetime), rotation=65) #works
plt.subplots_adjust(bottom=0.2)
plt.title(('Rolling Statistics for Cycle Times, ' + 'window = ' + str(offset) + ', min_periods = ' + str(min_periods)),
          fontdict={'fontweight':'bold', 'fontsize':17})
plt.show()

# Perform Dickey-Fuller test:
# print('Results of Dickey-Fuller Test:')
# dftest = adfuller(pbc_data, autolag='AIC')
# dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
# for key, value in dftest[4].items():
#     dfoutput['Critical Value (%s)' % key] = value
# print(dfoutput)
#
# if dfoutput['Test Statistic'] > dfoutput['Critical Value (1%)']:
#     print('Test statistic is greater than critical value (1%). Time series is NON-STATIONARY.')
# else:
#     print('Test statistic is less than critical value (1%). Time series is STATIONARY.')

#print('Last values of rolling cycle times mean: ')
#print(rolmean[-(int(math.ceil(window * 0.75))):])
#print(rolmean[-window:-(int(math.ceil(window * 0.5)))])

#print('Last values of rolling cycle times Upper Control Limits: ')
#print(rolmean[-(int(math.ceil(window * 0.75))):])
#print(rolucl[-window:-(int(math.ceil(window * 0.5)))])
