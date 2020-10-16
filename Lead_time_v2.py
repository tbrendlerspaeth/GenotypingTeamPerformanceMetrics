"""
Captures and analyses data for lead time for plates processed by a genotyping team.
created on 2020.08.11
"""

import pandas as pd
import os
import matplotlib.pylab as plt
import numpy as np
import datetime


class LeadTime:

    def __init__(self, genotype_assignments):
        df_data = self.data_process(genotype_assignments)

        # CREATING MULTIPLE DFs TO SORT RECEIVED AND UPLOAD DATA SEEMS UNNECESSARY AND CONFUSING
        # Can we just work with one df? Plate Barcode, Plate Received Date, Assignment Date, Animal Name
        # (Mouse Name must be handled - changed to Animal Name in data_process ? Seems a legit solution
        # Then concatenate Animal Name with Plate Barcode to create Sample

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
                # MUST HANDLE ANIMAL/MOUSE NAME COLUMN NAMING ISSUE
                return pd.read_csv(data)

            else:
                folder_path = data
                data = pd.DataFrame()
                for foldername, subfolders, filenames in os.walk(folder_path):
                    for file in filenames:
                        file_path = foldername + '\\' + file
                        data = data.append(pd.read_csv(file_path))
                        # MUST HANDLE ANIMAL/MOUSE NAME COLUMN NAMING ISSUE
                return data


    def lead_time_plot_plates(self, window, min_periods):

        # Let's create an approximation of a Performance Behaviour Chart
        pbc_data = self.lead_time_data
        pbc_data.set_index('Plate Received Date', inplace=True)
        pd.to_datetime(pbc_data.index)
        pbc_data = pbc_data.loc['20200101':]
        window = window
        min_periods = min_periods
        xdata = pbc_data.index
        ydata = pbc_data['Lead time'].dt.days
        plt.scatter(xdata, ydata, color='black', s=10, label='Plate', marker='+', alpha=0.5)

        # Create rolling statistics
        pbc_lead_times = pbc_data['Lead time'].dt.days
        rolmean = pbc_lead_times.rolling(window=window, min_periods=min_periods).mean()
        rolmedian = pbc_lead_times.rolling(window=window, min_periods=min_periods).median()
        rolstd = pbc_lead_times.rolling(window=window, min_periods=min_periods).std()
        rolucl = rolmean + 2 * rolstd

        # Plot rolling statistics:
        plt.plot(rolmean, color='green', label='Rolling Mean')
        plt.plot(rolmedian, color='blue', label='Rolling Median')
        # plt.plot(rolucl, color='red', label='Rolling Upper Control Limit (mean+2*std)')
        delta_time = pbc_data['Latest upload date'].max() - pbc_data.index[0]
        x_coords, y_coords = [pbc_data.index[0], pbc_data['Latest upload date'].max()], [delta_time.days, 0]
        print("x_coords:", x_coords)
        print("y_coords:", y_coords)
        plt.plot(x_coords, y_coords, color='red', linestyle='--', alpha=0.5, label='Number of days preceding most recent upload date')
        plt.xlabel("Date plate received", fontdict={'fontsize': 16})
        plt.ylabel("Lead time (Days)", fontdict={'fontsize': 16})
        plt.legend(loc='best', fontsize=14, facecolor='white', framealpha=1)
        plt.grid(axis='y')
        ydata_max = ydata.max()
        plt.yticks(np.arange(0, int(delta_time.days + 10), 10))
        plt.xticks(np.arange(pbc_data.index[0], pbc_data.index[-1], datetime.timedelta(weeks=2)).astype(datetime.datetime), rotation=65)
        plt.subplots_adjust(bottom=0.2)
        plt.title('Rolling Statistics for Plate Lead Times',
                  fontdict={'fontweight': 'bold', 'fontsize': 20})
        plt.show()


    def print_lead_time_data(self):
        print(self.lead_time_data)



if __name__=="__main__":
    print("Program running...")
    genotype_assignments = r"Z:\Genotyping\T121_metrics\Raw data\Genotype Assignments Reports\Weekly Genotype Assignments Reports"
    genotype_assignments = LeadTime(genotype_assignments = genotype_assignments)
    genotype_assignments.print_lead_time_data()
    genotype_assignments.lead_time_plot_plates(window='7D', min_periods=10)
