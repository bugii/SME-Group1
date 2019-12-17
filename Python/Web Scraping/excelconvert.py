import pandas as pd
import re
from functions import file_to_stringlist

def write_to_excel(*args, filename="Excel/excel_output.xlsx", skip_empty_files=False):
    # As it says: Writes the input to an excel file in the Excel folder. ekip_empty_files means that it will not
    # write an excel file if the input lists are empty.

    # Creating the dataframe
    df = pd.DataFrame()

    if skip_empty_files and len(args[0])==0:
        print("Empty input for excel writer. Skipping and proceeding to next input.")
    else:
        for idx, val in enumerate(args):
            df[idx] = val
        df.to_excel(filename, index=False)

def convert_to_excel(filename, date_as_int=False, interpreted=False):
    # Converts a given file into an excel sheet. date_as_int converts 2019-11-30 to 20191130 (for easier sorting).
    list = file_to_stringlist(filename, "")

    # Creating output columns
    list1 =[]
    list2 =[]
    list3 =[]
    list4 = []
    list5 = []
    if interpreted:
        data_indices = [0, 3, 4, 1, 2]
    else:
        data_indices = [0, 1, 2]
    temp_val = ""
    excel_name=""

    for idx, val in enumerate(list):
        if val.startswith("/"):
            if excel_name == "":
                excel_name = "Excel/" + val[val.rindex("/") + 1:] + ".xlsx"
            else:
                write_to_excel(list1, list2, list3, filename=excel_name, skip_empty_files=True)
                list1.clear()
                list2.clear()
                list3.clear()
                list4.clear()
                list5.clear()
                excel_name = "Excel/" + val[val.rindex("/") + 1:] +".xlsx"
        else:
            temp_val = val.split("::")
            if interpreted:
                temp_val = [element for item in temp_val for element in item.split(':')]
            list1.append(int(temp_val[data_indices[0]])) # Total dependencies
            if date_as_int:
                temp_list = temp_val[data_indices[1]].split("-")
                temp_val2 = temp_list[0] + temp_list[1] + temp_list[2]
                list2.append(int(temp_val2)) # Release dates
            else:
                list2.append(temp_val[data_indices[1]])  # Release dates
            list3.append(int(temp_val[data_indices[2]])) # Number of bugs
        if interpreted:
            list4.append(int(temp_val[data_indices[3]])) # Apache dependencies
            list5.append(int(temp_val[data_indices[4]]))  # Apache commons dependencies
    if excel_name=="":
        write_to_excel(list1, list2, list3, list4, list5, skip_empty_files=True)





