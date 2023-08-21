

#!/usr/bin/env python3
import os
import csv
from tabulate import tabulate
from get_stats.exts import exts_dict
import chardet
import pandas as pd
import asciibars as a_bars

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
            dirnames.remove("node_modules")
        if "venv" in dirnames:
            dirnames.remove("venv")
        
        os.chdir(dirpath)
        for file in filenames:
            root, ext = os.path.splitext(file)
            if ext not in exts_tresor:
                continue
            if file == "stats.txt":
                continue
            if file == "package.json":
                continue
            else:
                file_tresor.append([file, count_lines(file), exts_tresor[ext]])
            
    file_tresor = sorted(file_tresor, key=lambda x: x[1], reverse=True)
    
    lang_df = make_lang_df(file_tresor)
    lang_chart = make_lang_chart(lang_df)
    table = make_table(file_tresor)
    stat_file = make_stat_file(path, table, lang_chart)
    
    
    

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

def make_lang_df(file_tresor):
    df = pd.DataFrame(file_tresor, columns=["Filename", "Lines", "Language"])
    lang_df = df.groupby('Language')['Lines'].sum().reset_index()
    
    total_lines = lang_df['Lines'].sum()
    lang_df['Percentage'] = round((lang_df['Lines'] / total_lines) * 100, 2)
    
    lang_df = lang_df.sort_values(by='Percentage', ascending=False)
    return lang_df


def make_stat_file(path, table, lang_chart):
    stats_path = os.path.join(path, "stats.txt")
    with open(stats_path, "w") as stats_file:
        stats_file.write("\n\n")
        stats_file.write(lang_chart)  
        stats_file.write("\n\n") 
        stats_file.write(table)

 
import io
import sys

def make_lang_chart(lang_df):
    data = []
    for _, row in lang_df.iterrows():
        data.append((str(row['Language']), float(row['Percentage'])))
          
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    a_bars.plot(data, unit='▓', neg_unit='░')
    sys.stdout = old_stdout

    return new_stdout.getvalue()
    
    
if __name__ == "__main__":
    main()