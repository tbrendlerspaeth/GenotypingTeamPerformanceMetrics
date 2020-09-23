import pandas as pd
import matplotlib.pyplot as plt


plates_received = pd.read_csv("Plates_received_01-01-2020_to_22-09-2020.csv")
plates_received = plates_received[plates_received['Plate Barcode'].str[0] != 'T']
plates_received['Assignment Date'] = pd.to_datetime(plates_received['Assignment Date'])
plates_received.sort_values(by='Assignment Date', inplace = True)

weekly_plates_received = plates_received.groupby(plates_received['Assignment Date'].dt.weekofyear)['Plate Barcode'].count()
window = 5
rolling_received_sum = weekly_plates_received.rolling(window=window).mean()


plt.bar(plates_received['Assignment Date'].dt.weekofyear.drop_duplicates(), weekly_plates_received, color='red', label="Weekly number of plates received")
plt.plot(rolling_received_sum, color='blue', label="Rolling mean plates received per week, window=" + str(window))
weeks = plates_received['Assignment Date'].dt.weekofyear.drop_duplicates()
weeks = list(weeks.drop_duplicates())
plt.xticks(weeks)
plt.xlabel("Week of Year 2020", fontdict={'fontsize': 16})
plt.ylabel("Number of plates received", fontdict={'fontsize': 16})
plt.title("T121 Number of plates received per week of 2020 with rolling average", fontdict={'fontweight': 'bold', 'fontsize': 20})
plt.legend(loc='best', fontsize=14, facecolor='white', framealpha=1)
plt.show()


daily_plates_received = plates_received.groupby(plates_received['Assignment Date'].dt.date)['Plate Barcode'].count()

x = plates_received['Assignment Date'].dt.date.drop_duplicates()
y = daily_plates_received
plt.bar(x, y, color='blue', label="Daily number of plates received")


df = plates_received.groupby(plates_received['Assignment Date'].dt.date)['Plate Barcode'].count().reset_index().sort_values('Assignment Date')
print(df.head())
df['Assignment Date'] = pd.to_datetime(df['Assignment Date']) # THIS IS SO IMPORTANT FOR THIS NONSENSE TO WORK. TOOK ME AN HOUR TO GET HERE.
df.set_index('Assignment Date', inplace=True)
print(df.head())

rolling_received_sum = df.rolling(window='7D', min_periods= 2).mean()
plt.plot(rolling_received_sum, color='red', label="Rolling sum number of plates received per day")
plt.legend(loc='best', fontsize=14, facecolor='white', framealpha=1)
plt.xlabel("Date", fontdict={'fontsize': 16})
plt.ylabel("Number of plates received", fontdict={'fontsize': 16})


plt.show()
