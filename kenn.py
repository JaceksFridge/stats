


import os
import csv
from tabulate import tabulate

def main():
    
    file_tresor = {}
    # file_list = []
    
    path = os.getcwd()
    for dirpath, dirnames, filenames in os.walk(path):
 
        if ".git" in dirnames:
            dirnames.remove(".git")
        if "myenv" in dirnames:
            dirnames.remove("myenv")
        if "node_modules" in dirnames:
            dirnames.remove("node_modules")
            
        os.chdir(dirpath)
        for file in filenames:
            
            file_tresor[file] = count_lines(file)
            # file_list.append([file, count_lines(file)])
        
    write = stat_file(path, file_tresor)
    # term = print_term(file_tresor)
    print(file_tresor)



def print_term(file_list):
    headers = ["file", "lines"]
    print(tabulate(file_list, headers, tablefmt='rst'))

    

def stat_file(path, file_tresor):
    
    stats_path = os.path.join(path, "stats.txt")
    
    with open(stats_path, "w", newline="") as print_file:
        writer = csv.DictWriter(print_file, fieldnames=["file", "lines"])
        writer.writeheader()
        
        for file, lines in file_tresor.items():
            if lines < 1:
                lines = 0
            if file != "stats.txt":
                writer.writerow({"file": file, "lines": lines})





def count_lines(file):
    count = 0
    with open(file, "r") as open_file:

        for line in open_file:
            if line.strip() == "":
                continue
            elif line.startswith("#"):
                continue
            else:
                print(line)
                count += 1

        return count
    
    
    
if __name__ == "__main__":
    main()