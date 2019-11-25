import re   #regular expression
from pathlib import Path

def read_gradle(read):
    #variables
    depbol = False
    dependencies = []   #list to keep the dependencies
    brackets = 0    # to know how many brackets are open
    namefile = "build.gradle"
    #code:
    '''   
    file= open(filepath + namefile,"r") #open the build.gradle in read only
    if file.mode == "r":  # if we are in read mode
        read= file.readlines()          #we copy the context of the file in line
        file.close()                       #we close the file
    '''
    for line in read:   #while neof line
        line = re.sub("(\n|\[|\]|(\/\/.*))","",line) #we change line break or  "[" or this "]" for ""
        if depbol:
            if re.sub(" ","",line) != "":
                if re.sub(" ", "", line)[-1] == "{":
                    brackets += 1
                if re.sub(" ","",line)=="}":
                    if brackets == 0:
                        depbol = False          # comprobamos que hemos acabado el bloque de dependencias
                    else:
                        brackets -= 1
                elif re.search("([iI]mplementation|[cC]ompile) group",line): # group
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



                elif re.search("([iI]mplementation|[cC]ompile) files", line): #encuentra files
                    depen = re.sub("(.*files|\'|,|\(|\))","",line) # quita todo lo anterior a files y "'","(",")" y ","
                    depen = depen.split() # separa en una lista el string depen
                    for dep in depen:       #recorre el array
                        dep = re.sub(".*/","",dep)  #le quitamos el directorio (hasta la última barra)
                        aux = ["None", dep, "None"] #añadimos dependencia con solo nombre y valores vacios en los otros campos
                        if aux not in dependencies: #añadimos a la lista
                            dependencies.append(aux)

                elif re.search("([iI]mplementation|[cC]ompile) fileTree\(", line):

                    line = re.sub(".*(?=(dir:))", "", line)

                    line = re.sub("(\,|\[|\]|\'|\))", "", line)

                    line = line.split()

                    for i in line:

                        if i == "dir:":

                            dir = line[line.index(i) + 1]

                        elif i == "include:":

                            exten = line[line.index(i) + 1]
                    if re.search("\*\..*",exten):                        #si el tipo de dependencia nos habla de una extension (es decir que sea [loquesea] . algo
                        for filename in Path("./" + dir).rglob(exten):  #hacemos una busqueda recursiva dentro del directorio buscamdo la extension indicada
                            name = str(filename)                        #hacemos casting de filename a string porque al parecer no lo era antes
                            aux = ["None",re.sub(".*\\\\","",name),"None"]  #dependencia lo mismo de files
                            if aux not in dependencies:
                                dependencies.append(aux)
                    else:
                        aux = ["None",re.sub(".*/","",exten),"None"]    #si no es de tipo extension y directamente nos da el archivo or whatever lo pasamos directamente en el mismo formato
                        if aux not in dependencies:
                            dependencies.append(aux)
                elif re.search(" libs\.",line):
                    depen = re.sub("(.*libs\.)|(\).*)","",line)
                    aux = ["None", re.sub(" ","",depen), "None"]
                    if aux not in dependencies:
                        dependencies.append(aux)
                elif re.search("project\(\':",line):
                    depen = re.sub("(.*project\(\')|(\'\).*)", "", line)
                    aux = ["None", re.sub(" ","",depen), "None"]
                    if aux not in dependencies:
                        dependencies.append(aux)

                elif re.search("([iI]mplementation|[cC]ompile) (\'|\").*:.*:.*(\'|\")", line):
                    depen = re.sub(".*(\'|\")(?=.*(\'|\"))", "", line)
                    depen = re.sub("(\'|\").*", "", depen)
                    depen = re.split(":", depen)
                    if depen not in dependencies:
                        dependencies.append(depen)



        else:
            if re.sub(" ","",line) == "dependencies{":
                depbol = True
    '''
    file= open("Dependencies.txt","w+")
    file.write("Group:\tName:\tVersion:\n")
    for i in range(len(dependencies)):
        string = "\t"
        string = string.join(dependencies[i])
        string += "\n"
        file.write(string)

    file.close()
    '''
    return (dependencies)

def get_number_dependencies(string_list):
    auxlist = read_gradle(string_list)
    return len(auxlist)