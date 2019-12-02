from functions import file_to_stringlist
import operator

def median_from_file(filename):
    # Calculates the median Dependency value from a file from the Dependencies folder.
    line_list = file_to_stringlist(filename, "Dependencies/")
    for idx, val in enumerate(line_list):
        k = -1
        while val[k] != " ":
            k -=1
        line_list[idx] = int(val[k+1:])
    line_list = (sorted(line_list))
    return line_list[int(len(line_list)/2)]

def median_calc(filename):
    # Returns a list of tuples with the project name and its respective dependencies.
    output_list = []
    line_list = file_to_stringlist(filename, "")
    for idx, val in enumerate(line_list):
        if idx < len(line_list)-2 and val.startswith("/") and line_list[idx+1][0].isdigit():
            project_name = val[val.rindex("/")+1:]
            temp_dep = median_from_file(project_name + ".txt")
            output_list.append((project_name, temp_dep))
    output_list.sort(key=operator.itemgetter(1))
    return output_list


