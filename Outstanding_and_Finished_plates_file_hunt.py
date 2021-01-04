"""
This program takes an Assay Samples with Genotype Mouse Database Report file path
to return a list of plates which can be set to Status: Finished as well as a list
of outstanding samples.

created by TABS
"""


import pandas as pd
import os
from datetime import date


class assay_samples_genotype:
    def __init__(self, ass_samples_gen_report_path):

        ass_samples_gen_report = pd.read_csv(ass_samples_gen_report_path)

        # Filter out Transnetyx plates
        ass_samples_gen_report = ass_samples_gen_report[ass_samples_gen_report['Plate Barcode'].str[0] != 'T']


        # Filter out re-arrayed plates
        ass_samples_gen_report = ass_samples_gen_report[ass_samples_gen_report['Status'] != 'Rearrayed']


        # Remove alleles and genotypes not required for unfinished sample detection
        removal_texts = ['| Kdm5b(.1):Untested']
        for text in removal_texts:
            ass_samples_gen_report['Latest Genotype'] = ass_samples_gen_report['Latest Genotype'].apply(
                lambda x: self.allele_genotype_remove(latest_genotype=x, removal_text=text))

        self.ass_samples_gen_report = ass_samples_gen_report


        # Filter by "Untested" or "Retest" in Latest Genotype to obtain unfinished samples
        self.unfinished_samples = self.ass_samples_gen_report[self.ass_samples_gen_report['Latest Genotype'].str.contains('Retest') |
                                                        self.ass_samples_gen_report['Latest Genotype'].str.contains('Untested')]


        # Get list of unfinished plates
        self.unfinished_plates_list = self.unfinished_samples['Plate Barcode'].drop_duplicates(keep='first').tolist()


        # Create finished plates df
        finished_plates = self.ass_samples_gen_report[~self.ass_samples_gen_report['Plate Barcode'].isin(self.unfinished_plates_list)]
        finished_plates = finished_plates[['Plate Barcode', 'Status', 'Category']]
        finished_plates.drop_duplicates(keep='first', inplace=True)
        finished_plates = finished_plates[finished_plates['Status'] != 'Plate Finished']
        finished_plates['Checked by:'] = ''
        finished_plates["Set to 'Finished'?"] = ''
        finished_plates['Comments'] = ''
        self.finished_plates_df = finished_plates


        # Create unfinished samples df
        # order by received date, then plate, then well sample? can we do that?
        columns = ['Animal Name', 'Latest Genotype', 'Plate Barcode', 'Well Position', 'Plate Location', 'Category', 'Plate Received Date']
        unfinished_samples = self.unfinished_samples[self.unfinished_samples['Plate Barcode'].str[0] != 'T']
        unfinished_samples['Plate Received Date'] = pd.to_datetime(unfinished_samples['Plate Received Date'])
        unfinished_samples.sort_values(by=['Plate Received Date', 'Plate Barcode', 'Well Position'], ascending=True, inplace=True)
        self.unfinished_samples_df = unfinished_samples[columns]


    def allele_genotype_remove(self, latest_genotype, removal_text):
        """Removes a specified text if present in a Latest Genotype column field."""
        if removal_text in latest_genotype:
            latest_genotype_mod = latest_genotype.replace(removal_text, "")
            return latest_genotype_mod
        else:
            return latest_genotype


    def df_to_excel(self, dataframe, excel_filename, directory):
        """Saves a dataframe as an Excel file to a user specified folder with user specified file name."""
        os.chdir(directory)
        excel_filename = excel_filename + '.xlsx'
        writer = pd.ExcelWriter(excel_filename, engine='openpyxl')
        dataframe.to_excel(writer, header=True, index=False)
        writer.save()
        writer.close()


    def update_uf_samples(self, directory):

        dataframe = self.unfinished_samples_df
        dataframe['Assigned to:'] = ''
        dataframe['Completed?'] = ''
        dataframe['Comments'] = ''

        excel_filename = "Unfinished_Samples"
        uf_samples_path = directory + "\\" + excel_filename +'.xlsx'


        if not os.path.isfile(path=uf_samples_path):
            print("Unfinished_Samples file not found. Creating new file...")
            self.df_to_excel(dataframe=dataframe, excel_filename=excel_filename, directory=directory)

        else:
            print("Unfinished_Samples file present in file. Updating file...")
            old_df = pd.read_excel(uf_samples_path)
            old_columns = ['Animal Name', 'Plate Barcode', 'Assigned to:', 'Completed?', 'Comments']
            old_df = old_df[old_columns]
            print(old_df.head())

            new_df = dataframe
            new_df.drop(columns=['Assigned to:', 'Completed?', 'Comments'], inplace=True)

            final_df = new_df.merge(old_df, how='left', on=['Animal Name', 'Plate Barcode'])
            self.df_to_excel(dataframe=final_df, excel_filename=excel_filename, directory=directory)


if __name__=="__main__":
    # Read in data
    print("Doing stuff...")
    report_path = input("Paste in the file path of the Assay Samples with Genotype report: ").strip("\"\'")
    ass_report = assay_samples_genotype(ass_samples_gen_report_path=report_path)

    # Get number of finished plates
    print(ass_report.finished_plates_df['Plate Barcode'].count(), " finished plates found. \n")
    print(ass_report.finished_plates_df)
    print("\n\n")

    # Get number of unfinished plates and samples
    print(len(ass_report.unfinished_plates_list), " unfinished plates found. \n")
    print(len(ass_report.unfinished_samples_df), " unfinished samples found. \n")
    print(ass_report.unfinished_samples_df.head())

    # Generate/update Finished plates and Unfinished Samples Excel files
    dataframe = ass_report.finished_plates_df
    today = date.today()
    today = today.strftime("%d-%m-%Y")
    excel_filename = "Finished_plates_" + today
    directory = r"C:\Users\tbren\Documents\Python\Python scripts\Projects\T121_performance_metrics\GenotypingTeamPerformanceMetrics-master"
    # Finished plates to Excel file
    ass_report.df_to_excel(dataframe=dataframe, excel_filename=excel_filename, directory=directory)
    # Unfinished Samples to Excel file
    ass_report.update_uf_samples(directory=directory)
