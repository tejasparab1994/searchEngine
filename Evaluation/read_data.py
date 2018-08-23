from collections import defaultdict

def get_rel_judgements(path):
    rel_jugdements = defaultdict(list)
    rel_file = open(path,"r")
    raw_rel = rel_file.readlines()

    without_linebreak = []
    for line in raw_rel:
        without_linebreak.append(line.strip("\n"))

    splitted = []
    for line in without_linebreak:
        splitted.append(line.split(" "))

    for line in splitted:
        rel_jugdements[line[0]].append(line[2])

    return rel_jugdements

def get_result_data(file):
    f = open(file,"r")
    raw_data = f.readlines()
    eachline = []
    for item in raw_data:
        eachline.append(item.split("\n"))
    data = []
    for item in eachline[2:]:
        data.append([_f for _f in item[0].split(" ") if _f])
    return data
