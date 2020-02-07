"""
This script is designed to collect and analyse data relevant to the work performance of a genotyping
team from the folders were database uploads containing results are stored.
created by TABS
version 2020.01.26
"""

import os
import pandas as pd
import datetime


def entries_harvest():
    entries_folder = input(r'Enter folder path of a database entries folder: ')

    time_started = datetime.datetime.now()
    print("Time started: ", time_started.time())

    df_all_entries = pd.DataFrame()

    for foldername, subfolders, filenames in os.walk(entries_folder):
        for file in filenames:
            file_path = foldername + '\\' + file
            try:
                df_file = pd.read_excel(file_path)
            except PermissionError:
                print('PermissionError occurred with file: ', file)
            except:
                print('There was a problem with reading this file: ', file)

            df_all_entries = df_all_entries.append(df_file)

    df_all_entries.dropna(axis=0, how='all', inplace=True)
    df_all_entries.dropna(axis=1, how='all', inplace=True)
    df_all_entries.drop_duplicates(keep='first', inplace=True)




    time_all_entries = datetime.datetime.now()
    print("Time finished with generating 'df_all_entries': ", time_all_entries.time())



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
        print("'df_all_entries' does not contain a 'Plate Barcode' column.")


    try:
        df_t121 = df_all_entries[(df_all_entries['Plate'].str[0] != 'T') & (df_all_entries['Plate Barcode'].str[0] != 'T')]
    except KeyError:
        print("Key Error occurred when filtering T121 entries.")
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
        print("'df_t121 does not' does not contain a 'Plate' column.")
    df_t121_platebarcode = pd.DataFrame()
    try:
        df_t121_platebarcode = df_t121[['Plate Barcode']].dropna()
        df_t121_platebarcode.rename(columns={'Plate Barcode': 'Plate'}, inplace=True)
    except KeyError:
        print("'df_t121' does not does not contain a 'Plate Barcode' column.")
    total_t121_plates = len(df_t121_plate.append(df_t121_platebarcode).drop_duplicates())


    total_transnetyx_plates = 0
    try:
        df_transnetyx_plate = df_transnetyx[['Plate']].dropna()
    except KeyError:
        print("'df_transnetyx' does not contain a 'Plate' column.")
    df_transnetyx_platebarcode = pd.DataFrame()
    try:
        df_transnetyx_platebarcode = df_transnetyx[['Plate Barcode']].dropna()
        df_transnetyx_platebarcode.rename(columns={'Plate Barcode': 'Plate'}, inplace=True)
    except KeyError:
        print("'df_transnetyx does not' does not contain a 'Plate Barcode' column.")
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




    time_finished = datetime.datetime.now()
    elapsed_time = time_finished - time_started
    elapsed_time = divmod(elapsed_time.total_seconds(), 60)
    print('Time taken to generate data: ', round(elapsed_time[0]), 'minutes ', round(elapsed_time[1]),
          'seconds.')




    print('Total number of database entries: ', total_entries)

    print('Total number of T121 entries: ', total_t121_entries)
    print('Total number of Transnetyx entries: ', total_transnetyx_entries)

    print('Total number of T121 plates with uploads: ', total_t121_plates)
    print('Total number of Transnetyx plates with uploads: ', total_transnetyx_plates)

    print('Percentage of T121 entries which are retests: ', round(percent_retest_t121, 1), '%')
    print('Percentage of T121 entries which are failed: ', round(percent_failed_t121, 1), '%')

    print('Percentage of Transnetyx entries which are retests: ', round(percent_retest_transnetyx, 1), '%')
    print('Percentage of Transnetyx entries which are failed: ', round(percent_failed_transnetyx, 1), '%')



while True:
    entries_harvest()
