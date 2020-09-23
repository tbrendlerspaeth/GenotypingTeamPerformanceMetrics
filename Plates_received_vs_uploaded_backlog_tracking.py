"""
Let's generate a graph that shows the numbers of plates received and uploaded by week. Additionally, it
should also display the difference between effective in- and output as a measure of plate backlog. The data
will be obtained from database reports.
I think we're going to need a new dataframe with plates received and uploaded per week (or maybe even per day) and then received -
uploaded for each time point in fourth column. Then plot the whole thing.
"""

print("Importing libraries...")

import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
from matplotlib.dates import DateFormatter
import time

print("Doing exciting things...")

# Get plates database uploads
plates_uploaded = pd.read_csv('Genotype_Assignments_01-01-2020_to_22-09-2020.csv')

# Transnetyx plates must be eliminated
plates_uploaded = plates_uploaded[plates_uploaded['Plate Barcode'].str[0] != 'T']

# Get the dates in order
plates_uploaded['Assignment Date'] = pd.to_datetime(plates_uploaded['Assignment Date'])
plates_uploaded.sort_values(by='Assignment Date', inplace = True)

# Create df with number of plates UPLOADED per week
plates_uploaded.drop_duplicates('Plate Barcode', keep='last', inplace = True)
daily_plates_uploaded = plates_uploaded.groupby(plates_uploaded['Assignment Date'].dt.date)[
    'Plate Barcode']
daily_plates_uploaded = pd.DataFrame(daily_plates_uploaded.count())
daily_plates_uploaded.reset_index(inplace = True)
daily_plates_uploaded.rename(columns = {'Assignment Date':'Date', 'Plate Barcode':'Plates uploaded'}, inplace = True)


# Get plates received and order the data
plates_received = pd.read_csv('Plates_received_01-01-2020_to_22-09-2020.csv')
plates_received = plates_received[plates_received['Plate Barcode'].str[0] != 'T']
plates_received['Assignment Date'] = pd.to_datetime(plates_received['Assignment Date'])
plates_received.sort_values(by='Assignment Date', inplace = True)

# Create df with number of plates RECEIVED per week
weekly_plates_received = plates_received.groupby(plates_received['Assignment Date'].dt.date)[
    'Plate Barcode']
weekly_plates_received = pd.DataFrame(weekly_plates_received.nunique())
weekly_plates_received.reset_index(inplace = True)
weekly_plates_received.rename(columns = {'Assignment Date':'Date', 'Plate Barcode':'Plates received'}, inplace = True)

# Merge dfs
data = daily_plates_uploaded.merge(right = weekly_plates_received, how = 'outer')
data['Plates received'].fillna(0, inplace = True)
data['Plates uploaded'].fillna(0, inplace = True)
data.sort_values(by = 'Date', inplace = True)

# Received - uploaded
data['Plate gain'] = data['Plates received'] - data['Plates uploaded']

# Backlog size calculation
data['Backlog size'] = data['Plate gain'].cumsum()

data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace = True)

rolling_received_sum = data['Plates received'].rolling(window='7D').mean()
rolling_uploaded_sum = data['Plates uploaded'].rolling(window='7D').mean()

plt.plot(data.index, data['Backlog size'], color='black', label="Estimated number of unfinished plates")
plt.plot(data.index, rolling_received_sum, color='red', label='Rolling number of plates received per day')
# plt.plot(data.index, rolling_uploaded_sum, color='green')
plt.bar(data.index, data['Plate gain'], color='blue', label='Plates received - uploaded per day')
plt.xlabel("Date", fontdict={'fontsize':16})
plt.ylabel("Number of plates", fontdict={'fontsize':16})
plt.title("Plate Input vs Output tracking", fontdict={'fontweight':'bold', 'fontsize':20})
y_max = data['Backlog size'].max()
#plt.yticks(np.arange(0, int(y_max + y_max*0.2), 20))
plt.grid(axis='y')
plt.legend(loc = 'best', fontsize=14, framealpha=1, facecolor='white')
# plt.bar(data.index, data['Plates received'], color = 'red')
plt.show()


# do I want a rolling mean plates received by week? Or a sum by week? I reckon sum. Yeh, sum.
# if we have rolling sum of plates received, why not also have the same for plates uploaded? Yeh.



# weeks_uploaded = list(plates_uploaded['Assignment Date'].dt.weekofyear.drop_duplicates())
# print(weeks_uploaded)
# plt.bar(weeks_uploaded, weekly_plates_uploaded.nunique())
# plt.xticks(weeks_uploaded[::2])
# plt.show()

# weekly_plates_uploaded = plates_uploaded.groupby('Assignment Date').resample('W-Mon', on='Assignment Date').nunique().reset_index().sort_values(by = 'Assignment Date')
# print(weekly_plates_uploaded)

# plt.plot(weekly_plates_uploaded.unique().reset_index())
# plt.show()



