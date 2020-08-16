"""
Captures and analyses data for lead time for plates processed by a genotyping team.
created on 2020.08.11
"""

import pandas as pd
import os
import matplotlib.pylab as plt
import numpy as np


class LeadTime:

    def __init__(self, genotype_assignments):
        df_data = self.data_process(genotype_assignments)

        received_data = df_data[['Plate Barcode', 'Plate Received Date']]

        upload_data = df_data[['Plate Barcode', 'Assignment Date']]
        upload_data.rename(columns={'Assignment Date': 'Date uploaded'}, inplace=True)

        upload_data['Date uploaded'] = pd.to_datetime(upload_data['Date uploaded'])
        received_data['Plate Received Date'] = pd.to_datetime(received_data['Plate Received Date'])

        latest_uploads = upload_data.sort_values(by='Date uploaded').drop_duplicates('Plate Barcode', keep='last')
        latest_uploads.rename(columns={'Date uploaded': 'Latest upload date'}, inplace=True)

        received_data.drop_duplicates('Plate Barcode', inplace=True)
        received_data = received_data[received_data['Plate Barcode'].str[0] != 'T']

        lead_time_data = received_data.merge(latest_uploads)
        lead_time_data.dropna(axis=0, how='any', inplace=True)
        lead_time_data['Lead time'] = lead_time_data['Latest upload date'].subtract(lead_time_data['Plate Received Date'])
        lead_time_data.sort_values('Plate Received Date', ascending=True, inplace=True)
        self.lead_time_data = lead_time_data


    def data_process(self, data):
        if not data:
            return pd.DataFrame()

        else:
            if data.endswith(".csv"):
                data.strip("\"\'")
                return pd.read_csv(data)

            else:
                folder_path = data
                data = pd.Dataframe()
                for foldername, subfolders, filenames in os.walk(folder_path):
                    for file in filenames:
                        file_path = foldername + '\\' + file
                        data = data.append(pd.read_csv(file_path))
                return data


    def lead_time_plot(self, window, min_periods):

        # Let's create an approximation of a Performance Behaviour Chart
        pbc_data = self.lead_time_data
        pbc_data.set_index('Plate Received Date', inplace=True)
        pbc_data = pbc_data.loc['20190902':]
        window = window
        min_periods = min_periods
        x = pbc_data.index
        y = pbc_data['Lead time'].dt.days
        plt.scatter(x, y, color='blue', s=10, label='Plate', marker='+', alpha=0.5)

        # Create rolling statistics
        pbc_lead_times = pbc_data['Lead time'].dt.days
        rolmean = pbc_lead_times.rolling(window=window, min_periods=min_periods).mean()
        rolstd = pbc_lead_times.rolling(window=window, min_periods=min_periods).std()
        rolucl = rolmean + 2 * rolstd

        # Plot rolling statistics:
        plt.plot(rolmean, color='green', label='Rolling Mean')
        plt.plot(rolucl, color='red', label='Rolling Upper Control Limit (mean+2*std)')
        plt.xlabel("Date plate received", fontdict={'fontsize': 16})
        plt.ylabel("Lead time (Days)", fontdict={'fontsize': 16})
        plt.legend(loc='best', fontsize=14, facecolor='white', framealpha=1)
        plt.grid(axis='y')
        y_max = y.max()
        plt.yticks(np.arange(0, int(y_max + 10), 10))
        plt.title('Rolling Statistics for Lead Times, window = ' + str(window),
                  fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.show()


    def print_lead_time_data(self):
        print(self.lead_time_data)



if __name__=="__main__":
    genotype_assignments = r"Genotype_Assignments_02-09-2019_to_22-03-2020.csv"
    genotype_assignments = LeadTime(genotype_assignments = genotype_assignments)
    genotype_assignments.print_lead_time_data()
    genotype_assignments.lead_time_plot(window='7D', min_periods=10)
