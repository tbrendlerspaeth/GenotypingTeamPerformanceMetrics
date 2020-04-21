"""
Programme analyses and prints out performance statistics for a genotyping team.
Unlike the Database_entries_folder_performance_metrics programme, the relevant data
is obtained from a database report rather than the team network drive.
created by TABS
"""
print("Loading modules...\n")


import pandas as pd



class genotype_assignments:
    def __init__(self, gen_ass_report_path):
        """Processes a Genotype Assignments database report."""

        print("Reading file and generating data...\n")
        
        gen_ass_report = pd.read_csv(gen_ass_report_path)
        gen_ass_report.drop_duplicates(keep='first', inplace=True)
        gen_ass_report['Assignment Date'] = pd.to_datetime(gen_ass_report['Assignment Date'])

        self.all_entries = gen_ass_report

        self.transnetyx_entries = self.all_entries[self.all_entries['Plate Barcode'].str[0] == 'T']
   
        self.t121_entries = self.all_entries[self.all_entries['Plate Barcode'].str[0] != 'T']

        

    def whose_data(self, data_source): # can we rename this "data_group"?
        if data_source == "t121":
            return self.t121_entries

        elif data_source == "transnetyx":
            return self.transnetyx_entries

        elif data_source == "all":
            return self.all_entries

        else:
            print("Well, you've royally ballsed this up, haven't you?") # must find better solution for this problem
        

    def num_entries(self, data_source):
        return len(self.whose_data(data_source))


    def num_plates(self, data_source):
        return len(self.whose_data(data_source)['Plate Barcode'].drop_duplicates())


    def num_genotypes(self, data_source):
        return len(self.whose_data(data_source)['Assigned Genotype'].dropna())


    def num_mice(self, data_source):
        return len(self.whose_data(data_source)['Mouse Name'].drop_duplicates())


    def num_colonies(self, data_source):
        return len(self.whose_data(data_source)['Colony Prefix'].drop_duplicates())


    def oldest_date(self):
        return self.all_entries['Assignment Date'].dt.date.min()


    def newest_date(self):
        return self.all_entries['Assignment Date'].dt.date.max()


    def get_stats(self, data_source):
        
        print("Metrics from", self.oldest_date(), "to", self.newest_date(), "for", data_source, ":", end="\n\n")
        print("Number of", data_source,  "entries: ", self.num_entries(data_source))
        print("Number of", data_source, "plates with entries: ", self.num_plates(data_source))
        print("Number of", data_source, "mice with entries: ", self.num_mice(data_source))
        print("Number of", data_source, "genotype entries: ", self.num_genotypes(data_source))
        print("Number of", data_source, "colonies with entries: ", self.num_colonies(data_source))
        



if __name__=="__main__":

    while True:
    
        gen_ass_report_path = input("Please paste in the file path of the database report you wish to obtain stats for: ").strip("\"\'")
        # gen_ass_report_path = "Z:\Genotyping\T121_metrics\Raw data\Weekly Genotype Assignments Reports\Team121_Genotype_Assignments_06-04-2020_to_12-04-2020.csv".strip("\"")
        report = genotype_assignments(gen_ass_report_path=gen_ass_report_path)
        
        report.get_stats('t121')
        print('\n\n\n')
        #report.get_stats('transnetyx')
        #print('\n\n\n')
        #report.get_stats('all')




