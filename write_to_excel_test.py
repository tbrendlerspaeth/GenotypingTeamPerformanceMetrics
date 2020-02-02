import pandas as pd
import os
from openpyxl import load_workbook

plates_received = 'Plates received 1 Sept 2019 to 29 Jan 2020 db report.csv'

df_received = pd.read_csv(plates_received)



# This manages to create a new sheet with the data in the existing PBC template file.
# book = load_workbook('PBC Template.xlsx')
# writer = pd.ExcelWriter('PBC Template.xlsx', engine='openpyxl')
# writer.book = book
# df_received.to_excel(writer, sheet_name='data', columns=['Plate Barcode', '#Samples'], startrow=1,
#                   startcol=0, index=False)
# writer.save()

# This also manages to create a new sheet with the data in the existing PBC template file.
# Seems shorter and hence makes he above redundant.
with pd.ExcelWriter('PBC Template.xlsx', mode='a') as writer:
    df_received.to_excel(writer, sheet_name='PBC', columns=['Plate Barcode', '#Samples'], startrow=1,
                         startcol=0, index=False)



os.startfile('PBC Template.xlsx')