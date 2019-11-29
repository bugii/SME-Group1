import pandas as pd
import re
from functions import file_to_stringlist

def convert_to_excel(filename, date_as_int=False):
    # Converts a given file into an excel sheet. date_as_int converts 2019-11-30 to 20191130 (for easier sorting).

    list = file_to_stringlist(filename, "")

    # Creating the dataframe
    df = pd.DataFrame()

    # Creating output columns
    list1 =[]
    list2 =[]
    list3 =[]
    temp_val = ""

    for idx, val in enumerate(list):
        temp_val = val.split("::")
        list1.append(int(temp_val[0])) # Total dependencies
        if date_as_int:
            temp_list = temp_val[1].split("-")
            temp_val2 = temp_list[0] + temp_list[1] + temp_list[2]
            list2.append(int(temp_val2)) # Release dates
        else:
            list2.append(temp_val[1])  # Release dates
        list3.append(int(temp_val[2])) # Number of bugs

    #In this part we declare the colums an then we write in excel
    df['Total Dependencies']= list1
    df['Release Dates'] = list2
    df['Bugs']= list3

    df.to_excel('result.xlsx', index = False)






