



import os
import csv
from tabulate import tabulate

def main():
    
    path = os.getcwd()
    stats_path = os.path.join(path, "kenn.py")
    print(count_lines(stats_path))
    
    file_tresor = []
    
    for dirpath, dirnames, filenames in os.walk(path):
        
        if "myenv" in dirnames:
            dirnames.remove("myenv")
        if ".git" in dirnames:
            dirnames.remove(".git")
        
        
        
        os.chdir(dirpath)
        for file in filenames:
            
            if file == ".DS_Store":
                continue
            file_tresor.append([file, count_lines(file)])

    table = make_table(file_tresor)
    
    

def count_lines(file):
    count = 0
    try:
        with open(file, "r") as open_file:

            for line in open_file:
                if line.strip() == "":
                    continue
                elif line.startswith("#"):
                    continue
                else:
                    count += 1
            
    except Exception as e:
        print(f"Error reading file {file}: {e}")
        return None
    
    return count


def make_table(file_tresor):
    headers =["files","lines"]
    print(tabulate(file_tresor, headers, tablefmt="rst"))    
    
    
if __name__ == "__main__":
    main()