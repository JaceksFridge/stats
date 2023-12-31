

#!/usr/bin/env python3
import io
import sys
import os
import csv
import re
from tabulate import tabulate
from get_stats.exts import exts_dict
import chardet
import pandas as pd
import asciibars as a_bars

exts_tresor = exts_dict()
table_size = 25

def main():
    
    path = os.getcwd()
    
    file_tresor = []
    hook_tresor = []
    
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
                hook_count = count_hooks(file)
                if hook_count['all hooks'] == 0:
                    continue
                else:
                    hook_tresor.append(list(hook_count.values()))
                
    og_length = len(file_tresor)
    file_tresor = sorted(file_tresor, key=lambda x: x[1], reverse=True)[:table_size]
    cs_length = len(file_tresor)
    hook_tresor = sorted(hook_tresor, key=lambda x: x[0], reverse=True)
    
    
    lang_df = make_lang_df(file_tresor)
    lang_chart = make_lang_chart(lang_df)
    hooks_table = make_hooks_table(hook_tresor)
    files_table = make_files_table(file_tresor)
    stat_file = make_stat_file(path, files_table, hooks_table, lang_chart, og_length, cs_length)
    
    
    

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



def make_files_table(file_tresor):
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


def make_stat_file(path, files_table, hooks_table, lang_chart, og_length, cs_length):
    stats_path = os.path.join(path, "stats.txt")
    with open(stats_path, "w") as stats_file:
        stats_file.write("\n\n")
        stats_file.write(lang_chart)
        stats_file.write("\n\n") 
        stats_file.write(files_table)
        stats_file.write(f"\n\n * showing {cs_length}/{og_length} files")
        stats_file.write("\n * run 'change_table' to change view")
        stats_file.write("\n\n")
        stats_file.write("\n\n")
        stats_file.write(hooks_table)

 

# Bar Chart 1
def make_lang_chart(lang_df):
    data = []
    for _, row in lang_df.iterrows():
        data.append((str(row['Language']), float(row['Percentage'])))
          
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    a_bars.plot(data, unit='▓', neg_unit='░', neg_max=100, count_pf='%')
    sys.stdout = old_stdout

    return new_stdout.getvalue()


def count_hooks(file):
    hook_count = {
        "all hooks": 0
    }
    hook_patterns = {
        "useState": r"const \[\w+\s*,\s*\w+\]\s*\=\s*useState\([^)]*\)",
        "useEffect": r"useEffect\(\s*\(\)\s*=>\s*\{(?:[^}]+|\n)+\}(,\s*\[.*?\]\s*)?\)",
        "useContext": r"const\s*([\w\s{},]+)\s*=\s*useContext\(\s*[-a-zA-Z0-9_]+\s*\)",
        "otherHooks": r"\buse(?!State\b|Effect\b|Context\b)(Callback|DebugValue|DeferredValue|Id|ImperativeHandle|InsertionEffect|LayoutEffect|Memo|Reducer|Ref|SyncExternalStore|Transition)\b",
        "customHooks": r"\buse(?!State\b|Effect\b|Context\b|Callback\b|DebugValue\b|DeferredValue\b|Id\b|ImperativeHandle\b|InsertionEffect\b|LayoutEffect\b|Memo\b|Reducer\b|Ref\b|SyncExternalStore\b|Transition\b)[A-Z]\w+\("
    }
    
    with open(file, "r") as file:
        content = file.read()
        
        for hook, pattern in hook_patterns.items():
            matches = re.findall(pattern, content)
            hook_count[hook] = len(matches)
            hook_count["all hooks"] += len(matches)
    return hook_count


# Hooks Table
def make_hooks_table(hook_tresor):
    headers =["all hooks","useState","useEffect","useContext","otherHooks","customHooks"]
    table = tabulate(hook_tresor, headers, tablefmt="presto")
    return table


def change_table():
    
    row_number = input("How many rows do you want to show?")
    table_size = row_number
    print(table_size)

    
    
if __name__ == "__main__":
    main()