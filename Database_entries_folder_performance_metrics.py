"""
This script is designed to collect and analyse data relevant to the work performance of Team 121
from the database entries folder.

created by TABS

version 2020.01.11

"""

import os
import pandas as pd
import datetime


def entries_harvest():
    entries_folder = input(r'Enter folder path of a database entries folder: ')

    time_started = datetime.datetime.now()
    df_all_entries = pd.DataFrame()

    for foldername, subfolders, filenames in os.walk(entries_folder):
        for file in filenames:
            file_path = foldername + '\\' + file
            try:
                df_file = pd.read_excel(file_path)
            except:
                print('ALERT: Exception file: ', file)

            df_all_entries = df_all_entries.append(df_file)
    df_all_entries.dropna(axis=0, how='all', inplace=True)
    df_all_entries.dropna(axis=1, how='all', inplace=True)
    df_all_entries.drop_duplicates(keep='first', inplace=True)

    df_transnetyx = pd.DataFrame()
    df_t121 = pd.DataFrame()
    try:
        for plate in df_all_entries['Plate Barcode']:
            try:
                if plate[0] == 'T':
                    transnetyx_plate = pd.DataFrame(df_all_entries[df_all_entries['Plate Barcode'] == plate])
                    df_transnetyx = df_transnetyx.append(transnetyx_plate, ignore_index=True)
                    df_transnetyx.drop_duplicates(keep='first', inplace=True)
                else:
                    t121_plate = pd.DataFrame(df_all_entries[df_all_entries['Plate Barcode'] == plate])
                    df_t121 = df_t121.append(t121_plate, ignore_index=True)
                    df_t121.drop_duplicates(keep='first', inplace=True)
            except:
                continue
    except KeyError:
        print("'df_all_entries' does not contain a 'Plate Barcode' column.")

    try:
        for plate in df_all_entries['Plate']:
            try:
                if plate[0] == 'T':
                    transnetyx_plate = pd.DataFrame(df_all_entries[df_all_entries['Plate'] == plate])
                    df_transnetyx = df_transnetyx.append(transnetyx_plate, ignore_index=True)
                    df_transnetyx.drop_duplicates(keep='first', inplace=True)
                else:
                    t121_plate = pd.DataFrame(df_all_entries[df_all_entries['Plate'] == plate])
                    df_t121 = df_t121.append(t121_plate, ignore_index=True)
                    df_t121.drop_duplicates(keep='first', inplace=True)
            except:
                continue
    except KeyError:
        print("'df_all_entries' does not contain a 'Plate' column.")

    time_finished = datetime.datetime.now()
    elapsed_time = time_finished - time_started
    elapsed_time = divmod(elapsed_time.total_seconds(), 60)
    print('Time taken for harvesting and editing: ', elapsed_time[0], 'minutes ', elapsed_time[1], 'seconds.')

    total_t121_entries = len(df_t121)
    total_transnetyx_entries = len(df_transnetyx)
    total_entries = len(df_all_entries)

    failed_t121 = len(df_t121[df_t121.Genotype.isin(['Failed', 'failed', 'failed ', ' Failed '])])
    retest_t121 = len(df_t121[df_t121.Genotype.isin(['Retest', 'retest', 'retest ', 'Retest '])])
    percent_failed_t121 = (failed_t121 / total_t121_entries) * 100
    percent_retest_t121 = (retest_t121 / total_t121_entries) * 100
    if total_transnetyx_entries > 0:
        failed_transnetyx = len(df_transnetyx[df_transnetyx.Genotype.isin(['Failed', 'failed', 'failed ', ' Failed '])])
        retest_transnetyx = len(df_transnetyx[df_transnetyx.Genotype.isin(['Retest', 'retest', 'retest ', 'Retest '])])
        percent_failed_transnetyx = (failed_transnetyx / total_transnetyx_entries) * 100
        percent_retest_transnetyx = (retest_transnetyx / total_transnetyx_entries) * 100
    else:
        print('The script found no entries with Transnetyx plates.')

    print('Total number of database entries: ', total_entries)
    print('Total number of T121 entries: ', total_t121_entries)
    print('Total number of Transnetyx entries: ', total_transnetyx_entries)
    print('Percentage of T121 retests: ', round(percent_retest_t121, 1))
    print('Percentage of T121 failed: ', round(percent_failed_t121, 1))
    print('Percentage of Transnetyx retests: ', round(percent_retest_transnetyx, 1))
    print('Percentage of Transnetyx failed: ', round(percent_failed_transnetyx, 1))


while True:
    entries_harvest()

"""
Suggestions for improvement, additions, alterations:
- Count number of different plate IDs to give some more indication of outputs for both T121 and Transnetyx
- Highlight the most common assay names
- Bring up the top 10 most error prone assay names for each walk.
- ?bring up the top 10 plates with the most errors associated with them?
- Turn the whole thing into a class? Using methods would cut down on repetition? Or maybe just use different functions?

"""
