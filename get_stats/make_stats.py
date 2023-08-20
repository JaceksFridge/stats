

#!/usr/bin/env python3
import os
import csv
from tabulate import tabulate
from get_stats.exts import exts_dict
import chardet



exts_tresor = exts_dict()


def main():
    
    path = os.getcwd()
    
    file_tresor = []
    
    for dirpath, dirnames, filenames in os.walk(path):
        
        if "myenv" in dirnames:
            dirnames.remove("myenv")
        if ".git" in dirnames:
            dirnames.remove(".git")
        if ".next" in dirnames:
            dirnames.remove(".next")
        if "node_modules" in dirnames:
            dirnames.remove("mode_modules")
        if "venv" in dirnames:
            dirnames.remove("venv")
        
        os.chdir(dirpath)
        for file in filenames:
            root, ext = os.path.splitext(file)
            if ext not in exts_tresor:
                continue
            else:
                file_tresor.append([dirnames +file, count_lines(file), exts_tresor[ext]])
            
    file_tresor = sorted(file_tresor, key=lambda x: x[1], reverse=True)
    table = make_table(file_tresor)
    stat_file = make_stat_file(path, table)
    
    
    

def count_lines(file):
    count = 0
    try:
        rawdata = open(file, "rb").read()
        encoding_result = chardet.detect(rawdata)
        charenc = encoding_result['encoding']

        with open(file, "r", encoding=charenc) as open_file:
            for line in open_file:
                if line.strip() == "":
                    continue
                elif line.startswith("#"):
                    continue
                else:
                    count += 1
    except Exception as e:
        print(f"Error reading file {file}: {e}")
        return 0

    return count



def make_table(file_tresor):
    headers =["files","lines","language"]
    table = tabulate(file_tresor, headers, tablefmt="rst")
    return table



def make_stat_file(path, table):
    stats_path = os.path.join(path, "stats.txt")
    with open(stats_path, "w") as stats_file:
        stats_file.write(table)
            
    
if __name__ == "__main__":
    main()