import pandas as pd
import re

file = open('output_interpreted.txt','r')
list = file.readlines()
file.close()
for elem in range(len(list)):
    list[elem -1]=re.sub("\n","",list[elem-1])
    list[elem -1]= list[elem - 1].split("::")


df = pd.DataFrame()

#create two colums
list1 = []
list2 =[]
for elem in range(len(list)):
    list1.append(list[elem-1][0])
    list2.append(list[elem-1][2])

#convert to b .to_excel('result.xlsx',index= False)
df['A'] = list1
df['B'] = list2
df.to_excel('result.xlsx', index = False)
print(list)
print(df)





#df = pd.read_csv('prueba.txt') # if your file is comma separated
#df.to_csv("prueba.txt",sep="::") # cambiar delimitador



#df = pd.read_table("C:\Users\miuzu\Desktop\scripx\pruebas.txt") # if your file is tab delimited

#df.to_excel('p1.xlsx') # To save to excel file

#df['State'] = list1[0::2] 
#df['Country'] = list1[1::2]
#df.to_excel('result.xlsx', index = False) 