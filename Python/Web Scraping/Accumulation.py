import functions

def accumulation_by_release(filename, directory):
    output_list = functions.file_to_stringlist(filename, directory)
    current_project = ""
    for i in output_list:
        if i.startswith("/"):
            current_project = i
        else:
            data_point = i.split("::")
            proceed_to_next_project = False
            for j in output_list:
                if j.startswith("/"):
                    proceed_to_next_project = (j == current_project)
                elif not proceed_to_next_project and len(j) != 0:
                    data_point_2 = j.split("::")
                    if functions.date1_greater_date2(data_point[1], data_point_2[1], or_equal=True):
                        data_point[0] = int(data_point[0]) + int(data_point_2[0])
                        data_point[2] = int(data_point[2]) + int(data_point_2[2])
                        proceed_to_next_project = True
            out_line = str(data_point[0]) + "::" + str(data_point[1]) + "::" + str(data_point[2])
            functions.write_to_txt(out_line, "output_accumulation.txt")
