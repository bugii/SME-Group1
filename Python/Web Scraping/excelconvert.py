import pandas as pd
import re

def convert_to_excel(filename):
    # We open the file and we read it and put in a list
    file = open(filename,'r')
    list = file.readlines()
    file.close()
    # we take out the spaces(\n) and we divide the list with the (::) patern
    for elem in range(len(list)):
        list[elem -1]=re.sub("\n","",list[elem-1])
        list[elem -1]= list[elem - 1].split("::")

    # We create the dataframe so lately
    df = pd.DataFrame()

    #create six colums
    list1 =[]
    list2 =[]
    list3 =[]
    list4 =[]
    list5 =[]
    list6 =[]

    # We introduce the information we want in the respective colums
    for elem in range(len(list)):
        list1.append(list[elem-1][0])
        list2.append(int(list[elem-1][2]))

    for elem in range(len(list1)):
        list3.append(list1[elem-1].split(":"))

    for elem in range(len(list3)):
        list4.append(int(list3[elem-1][0]))
        list5.append(int(list3[elem-1][1]))
        list6.append(int(list3[elem-1][2]))

    #In this part we declare the colums an then we write in excel
    df['Total Dependencies']= list4
    df['Apache']= list5
    df['Apache Commons']= list6
    df['Bugs']= list2
    df.to_excel('result.xlsx', index = False)






