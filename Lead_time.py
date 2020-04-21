"""
Script that generates lead time data for plates processed by a genoptying team.
created by TABS
version 2020.02.01

"""

import os
import pandas as pd
import datetime
import matplotlib.pylab as plt
import math
import numpy as np

# DELETE TRANSNETYX ENTRIES THEN SORT OLDEST TO NEWEST ON ASSIGNMENT DATE. ENSURE ASSIGNMENT DATE IS IN FORMAT %d/%m/%y
# BELOW FOR DATETIME CONVERSION

plates_received = 'Received Sept 2019 to 30-03-2020.csv'

df_received = pd.read_csv(plates_received)
df_received = df_received[['Plate Barcode', 'Assignment Date']]
df_received.rename(columns={'Plate Barcode': 'plate', 'Assignment Date': 'received'}, inplace=True)


# uploads_folder = input(r'Enter the folder path of your 2019 database uploads folder: ')
uploads_folder = r'\\file01-s0\team121\Genotyping\Database entries\2019'
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


# uploads_folder = input(r'Enter the folder path of your 2020 database uploads folder: ')
uploads_folder = r'\\file01-s0\team121\Genotyping\Database entries\2020'
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





# for i in df_final['received']:
#     i = datetime.datetime.strptime(i, '%d/%m/%y')
df_final['received'] = pd.to_datetime(df_final['received'], format='%d/%m/%Y')
df_final['latest upload'] = pd.to_datetime(df_final['latest upload'])
#df_final['received'] = datetime.datetime.strptime(df_final['received'], '%d/%m/%y')


df_final['cycle time'] = df_final['latest upload'].subtract(df_final['received'])

df_final_posonly = df_final[(df_final['cycle time'] >= datetime.timedelta(days=0))]




# df_final['received'] = df_final['received'].dt.date
df_final['latest upload'] = df_final['latest upload'].dt.date
# df_final['lead time'] = df_final['latest upload'].subtract(df_final['received'])

with pd.ExcelWriter('PBC Template.xlsx', mode='w') as writer:
    df_final_posonly.to_excel(writer, sheet_name='lead time data', startrow=1, startcol=0, index=False)

#writer.save()
#os.startfile('PBC Template.xlsx')




#print(df_final_posonly.head(20))

# window = 100
# pbc_data = df_final_posonly
# pbc_data.set_index('received', inplace=True)
# pbc_cycle_times = pbc_data['cycle time'].dt.days
#
# Create rolling statistics
# rolmean = pbc_cycle_times.rolling(window=window, center=True).mean()
# rolstd = pbc_cycle_times.rolling(window=window, center=True).std()
# rolucl = rolmean + 2 * rolstd
#
# Plot rolling statistics:
# plt.plot(pbc_cycle_times, color='blue', label='Lead Times')
# plt.plot(rolmean, color='green', label='Rolling Mean')
# plt.plot(rolucl, color='red', label='Rolling Upper Control Limit')
# plt.xlabel("Date")
# plt.ylabel("Lead time (Days)")
# plt.legend(loc='best')
# today = datetime.date.today()
# plt.title('Rolling Statistics for Lead Times, ' + str(today) + ', Window = ' + str(window))
# plt.show()


today = datetime.date.today()
pbc_data = df_final_posonly
pbc_data.set_index('received', inplace=True)
pbc_lead_times = pbc_data['cycle time'].dt.days
window = '7D'
min_periods = 10
x = pbc_data.index
y = pbc_data['cycle time'].dt.days
plt.scatter(x, y, color='blue', s=10, label='Plate', marker='+', alpha=0.5)


# Create rolling statistics
rolmean = pbc_lead_times.rolling(window=window, min_periods=min_periods).mean()
rolmedian = pbc_lead_times.rolling(window=window, min_periods=min_periods).median()
rolstd = pbc_lead_times.rolling(window=window, min_periods=min_periods).std()
rolucl = rolmean + 2 * rolstd

# Plot rolling statistics:

plt.plot(rolmean, color='green', label='Rolling Mean')
plt.plot(rolucl, color='red', label='Rolling Upper Control Limit (mean+2*std)')
plt.plot(rolmedian, color='blue', label='Rolling Median')
plt.xlabel("Date plate received", fontdict={'fontsize':16})
plt.ylabel("Lead time (Days)", fontdict={'fontsize':16})
plt.legend(loc='best', fontsize=14, facecolor='white', framealpha=1)
plt.grid(axis='y')
y_max = y.max()
plt.yticks(np.arange(0, int(y_max + 10), 10))
plt.title('Rolling Statistics for Lead Times, ' + str(today) + ', window = ' + str(window), fontdict={'fontweight':'bold', 'fontsize':20})
plt.show()


df_sept_dec_19 = pbc_data.loc['20190902':'20191231']
print('Lead time stats for Sept - Dec 2019: \n', df_sept_dec_19['cycle time'].describe(percentiles=[.25, .5, .75, 0.95]))

today = datetime.date.today()
df_2020 = pbc_data.loc['20200101':today]
print('Lead time stats for 2020: \n', df_2020['cycle time'].describe(percentiles=[.25, .5, .75, 0.95]))
pbc_data = df_final_posonly.loc['20190902':today]
