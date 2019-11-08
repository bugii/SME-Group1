import re   #regular expression

#variables
depbol = False
dependencies = []   #list to keep the dependencies
brackets = 0    # to know how many brackets are open
#code:
file= open("build.gradle","r") #open the build.gradle in read only
if file.mode == "r":  # if we are in read mode
    read= file.readlines()          #we copy the context of the file in line
    file.close()                       #we close the file
for line in read:   #while neof line
    line = re.sub("(\n|\[|\])","",line) #we change line break or  "[" or this "]" for ""
    if depbol:
        if re.sub(" ", "", line)[-1] == "{":
            brackets += 1
        if re.sub(" ","",line)=="}":
            if brackets == 0:
                depbol = False          # comprobamos que hemos acabado el bloque de dependencias
            else:
                brackets -= 1
        elif re.search("group",line): # group
            aux = [0,0,0]
            depen = re.sub(".*(?=(group:))", "", line)  #go to the expresion group: but we dont change it
            depen = re.sub("(\)|,)","",depen)
            depen = depen.split()   # convert the string into an array
            for elem in depen:
                if elem == "group:":
                    aux[0] = re.sub("'","",depen[depen.index(elem)+1])
                elif elem == "name:":
                    aux[1] = re.sub("'","",depen[depen.index(elem)+1])
                elif elem == "version:":
                    aux[2] = re.sub("'","",depen[depen.index(elem)+1])
            if aux not in dependencies:
                dependencies.append(aux)



        #elif re.search("files", line):     #wip

        #elif re.search("filetree", line):  #wip

        elif re.search("(\'|\").*:.*:.*(\'|\")", line):
            depen = re.sub(".*(\'|\")(?=.*(\'|\"))", "", line)
            depen = re.sub("(\'|\").*", "", depen)
            depen = re.split(":", depen)
            if depen not in dependencies:
                dependencies.append(depen)



    else:
        if re.sub(" ","",line) == "dependencies{":
            depbol = True

file= open("Dependencies.txt","w+")
file.write("Group:\tName:\tVersion:\n")
for i in range(len(dependencies)):
    string = "\t"
    string = string.join(dependencies[i])
    string += "\n"
    file.write(string)

file.close()