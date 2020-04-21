"""
This script is designed to collect and analyse data relevant to the work performance of a genotyping
team from the folders were database uploads containing results are stored.
created by TABS
version 2020.03.30
"""

print("Script loading libraries...\n")

import os
import pandas as pd
import datetime


def entries_harvest():
    entries_folder = input(r'Enter folder path of a database entries folder: ')

    time_started = datetime.datetime.now()
    print("\nDatabase entries harvest running. Time started: ", time_started.time())

    df_all_entries = pd.DataFrame()

    for foldername, subfolders, filenames in os.walk(entries_folder):
        for file in filenames:
            file_path = foldername + '\\' + file
            try:
                df_file = pd.read_excel(file_path)
                df_all_entries = df_all_entries.append(df_file)
            except PermissionError:
                print('PermissionError occurred with file: ', file)
            except:
                print('There was a problem with reading this file: ', file)

            

    df_all_entries.dropna(axis=0, how='all', inplace=True)
    df_all_entries.dropna(axis=1, how='all', inplace=True)
    df_all_entries.drop_duplicates(keep='first', inplace=True)




    #1
    #df_transnetyx = df_all_entries[(df_all_entries['Plate'].str[0] == 'T') |
    #                               (df_all_entries['Plate Barcode'].str[0] == 'T')]
    #df_t121 = df_all_entries[(df_all_entries['Plate'].str[0].isin(['S', 's', 'C', 'c'])) |
    #                         (df_all_entries['Plate Barcode'].str[0].isin(['S', 's', 'C', 'c']))]


    # 2
    df_transnetyx = df_all_entries[(df_all_entries['Plate'].str[0] == 'T')]
    try:
        df_transnetyx = df_transnetyx.append(df_all_entries[df_all_entries['Plate Barcode'].str[0] == 'T'])
    except KeyError:
        pass


    try:
        df_t121 = df_all_entries[(df_all_entries['Plate'].str[0] != 'T') & (df_all_entries['Plate Barcode'].str[0] != 'T')]
    except KeyError:
        df_t121 = df_all_entries[df_all_entries['Plate'].str[0] != 'T']



    df_gender = pd.DataFrame()

    try:
        df_gender = df_all_entries['Gender'].dropna()
    except KeyError:
        print("'df_all_entries' has no 'Gender' column. It seems no gender uploads could be found.")





    #total_t121_entries = len(df_t121) + len(df_gender)
    total_t121_entries = len(df_t121)
    total_transnetyx_entries = len(df_transnetyx)
    total_entries = len(df_all_entries)




    total_t121_plates = 0
    try:
        df_t121_plate = df_t121[['Plate']].dropna()
    except KeyError:
        pass
    df_t121_platebarcode = pd.DataFrame()
    try:
        df_t121_platebarcode = df_t121[['Plate Barcode']].dropna()
        df_t121_platebarcode.rename(columns={'Plate Barcode': 'Plate'}, inplace=True)
    except KeyError:
        pass
    total_t121_plates = len(df_t121_plate.append(df_t121_platebarcode).drop_duplicates())


    total_transnetyx_plates = 0
    try:
        df_transnetyx_plate = df_transnetyx[['Plate']].dropna()
    except KeyError:
        pass
    df_transnetyx_platebarcode = pd.DataFrame()
    try:
        df_transnetyx_platebarcode = df_transnetyx[['Plate Barcode']].dropna()
        df_transnetyx_platebarcode.rename(columns={'Plate Barcode': 'Plate'}, inplace=True)
    except KeyError:
        pass
    total_transnetyx_plates = len(df_transnetyx_plate.append(df_transnetyx_platebarcode).drop_duplicates())



    failed_t121 = len(df_t121[df_t121.Genotype.isin(['Failed', 'failed', 'failed ', ' Failed '])])
    failed_t121 = failed_t121 + len(df_gender.isin(['U', 'u']))

    retest_t121 = len(df_t121[df_t121.Genotype.isin(['Retest', 'retest', 'retest ', 'Retest '])])

    percent_failed_t121 = (failed_t121 / total_t121_entries) * 100
    percent_retest_t121 = (retest_t121 / total_t121_entries) * 100



    failed_transnetyx = 0
    retest_transnetyx = 0
    percent_failed_transnetyx = 0
    percent_retest_transnetyx = 0

    if total_transnetyx_entries > 0:
        failed_transnetyx = len(df_transnetyx[df_transnetyx.Genotype.isin(['Failed', 'failed', 'failed ', ' Failed '])])
        retest_transnetyx = len(df_transnetyx[df_transnetyx.Genotype.isin(['Retest', 'retest', 'retest ', 'Retest '])])
        percent_failed_transnetyx = (failed_transnetyx / total_transnetyx_entries) * 100
        percent_retest_transnetyx = (retest_transnetyx / total_transnetyx_entries) * 100
    else:
        print('The script found no entries with Transnetyx plates.')



    t121_mice = len(df_t121['Mouse'].drop_duplicates())
    transnetyx_mice = len(df_transnetyx['Mouse'].drop_duplicates())


    
    t121_genotypes = len(df_t121['Genotype'].dropna())
    transnetyx_genotypes = len(df_transnetyx['Genotype'].dropna())


    t121_colonies = df_t121['Mouse'].str[0:4]
    t121_colonies = len(t121_colonies.apply(lambda x: ''.join([i for i in str(x) if not i.isdigit()])).drop_duplicates())

    transnetyx_colonies = df_transnetyx['Mouse'].str[0:4]
    transnetyx_colonies = len(transnetyx_colonies.apply(lambda x: ''.join([i for i in str(x) if not i.isdigit()])).drop_duplicates())



    time_finished = datetime.datetime.now()
    elapsed_time = time_finished - time_started
    elapsed_time = divmod(elapsed_time.total_seconds(), 60)
    print('\nTime taken to generate data: ', round(elapsed_time[0]), 'minutes ', round(elapsed_time[1]),
          'seconds.')




    print('\nTotal number of database entries: ', total_entries)

    print('Total number of T121 entries: ', total_t121_entries)
    print('Total number of Transnetyx entries: ', total_transnetyx_entries)

    print('Total number of T121 plates with uploads: ', total_t121_plates)
    print('Total number of Transnetyx plates with uploads: ', total_transnetyx_plates)

    print('Percentage of T121 entries which are retests: ', round(percent_retest_t121, 1), '%')
    print('Percentage of T121 entries which are failed: ', round(percent_failed_t121, 1), '%')

    print('Percentage of Transnetyx entries which are retests: ', round(percent_retest_transnetyx, 1), '%')
    print('Percentage of Transnetyx entries which are failed: ', round(percent_failed_transnetyx, 1), '%')

    print('Total number of T121 mice with uploads: ', t121_mice)
    print('Total number of Transnetyx mice with uploads: ', transnetyx_mice)

    print('Total number of T121 uploaded genotpyes: ', t121_genotypes)
    print('Total number of Transnetyx genotypes: ', transnetyx_genotypes)

    print('Total number of T121 colonies: ', t121_colonies)
    print('Total number of Transnetyx colonies: ', transnetyx_colonies)


    
if __name__=="__main__":
    while True:
        entries_harvest()
