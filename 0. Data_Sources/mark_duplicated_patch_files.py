import difflib
import time
import os
import jellyfish
import re
import time
import math

import numpy as np
import multiprocessing
import multiprocessing.pool
import threading
import concurrent.futures
from functools import partial

# Enter the root folder path to start the comparison and output file location
root_folder = 'D4J_Correct_80NoDupl (592Files)'
output_file_path = 'Marked-dupliactes-all.txt'

# !!! YOU MUST RUN THIS SCRIPT FROM TERMINAL, PYTHON IDLE DON'T SUPPORT MULTI-THREAD EXECUTION

cpu_num = multiprocessing.cpu_count() - 1
print(f"CPU_NUM: {cpu_num}")
lock1 = threading.Lock()
lock2 = threading.Lock()
lock3 = threading.Lock()

def compare_files_sub(org_index, file1, file2):
    global identical_groups, group_id, lock1, lock2, lock3, perc_info

    lock1.acquire(timeout=1)
    # Print whole(rounded) percentages of comapred files
    perc_info['comp_files_num'] += 1
    percentage = int(perc_info['comp_files_num'] / (perc_info['num_files_to_compare'] / 100))
    if percentage > perc_info['old_perc']:
        perc_info['old_perc'] += 1
        tmp_time = time.time()+7200
        str_time = time.strftime('%H:%M:%S', time.gmtime(tmp_time-perc_info['start_time']))
        print()
        print(f"{percentage}%  <<  {perc_info['comp_files_num']}  num_compared_files  //  elapsed_time: {str_time}")
    lock1.release()

    lock3.acquire(timeout=1)
    # Check if the pair of files is already identified as identical
    if file1 in identical_groups and file2 in identical_groups:
        return
    lock3.release()
     
    # Optimization: to compare files only from same project_name but with different bug_id
    project_name_regex = re.search(r"(Closure|Math|Time|Lang|Chart|Mockito)[-\_]([0-9]+).*", file1)
    project_bugid = ""
    if project_name_regex:
        d4j_project_name = project_name_regex.group(1)
        bug_id =  project_name_regex.group(2)
        # if d4j_project_name+"-"+bug_id in file2 or not d4j_project_name in file2:
        if not d4j_project_name in file2:
            return

    lock2.acquire(timeout=2)
    with open(file1, 'r', encoding='latin-1') as f1, open(file2, 'r', encoding='latin-1') as f2:
        lines1 = f1.readlines()
        f1.seek(0)
        string1 = f1.read()
        lines2 = f2.readlines()
        f2.seek(0)
        string2 = f2.read()
    lock2.release()

    # faster to create process.Pool than create multiprocessing.Process and use multiprocessing.Queue to store result
    pool_proc = multiprocessing.Pool(1)
    result = pool_proc.apply(calculate_similarity_proc, args=(lines1, lines2, string1, string2))
    pool_proc.close()
    levenshtein_similarity_score = result['levenshtein']
    jaro_similarity_score = result['jaro']

    lock3.acquire(timeout=1)
    if levenshtein_similarity_score >= 0.80 or jaro_similarity_score >= 0.85:
        if file1 not in identical_groups and file2 not in identical_groups:
            group_id += 1
            identical_groups[file1] = group_id
            identical_groups[file2] = group_id
        elif file1 in identical_groups and file2 not in identical_groups:
            identical_groups[file2] = identical_groups[file1]
        elif file2 in identical_groups and file1 not in identical_groups:
            identical_groups[file1] = identical_groups[file2]
    lock3.release()
    
    
def calculate_similarity_proc(l1, l2, s1, s2):
    levenshtein_similarity_score = compute_levenshtein_similarity(l1, l2)
    jaro_similarity_score = jellyfish.jaro_similarity(s1, s2)
    return {'process_name': multiprocessing.current_process().name, 'levenshtein': levenshtein_similarity_score, 'jaro': jaro_similarity_score}
    

def compare_files(files_num, start_time):
    global files_to_compare, identical_groups, group_id, perc_info

    arr_comp_tmp = []
    for f in files_to_compare:
        arr_comp_tmp.append(f.split(os.sep)[-1])

    pool = multiprocessing.pool.ThreadPool(cpu_num)

    # Compare each pair of files
    for i in range(len(files_to_compare)):
        
        # Run processes in parallel
        # .map() will wait all processes to finish their work before jump to another .map()
        # .map_async() don't wait processes to finish their work and it is free to jump into another .map_async()
        part_func = partial(compare_files_sub, i, files_to_compare[i])
        pool.map_async(part_func, files_to_compare[i+1:len(files_to_compare)])
       
    pool.close()
    pool.join()


def compute_levenshtein_similarity(lines1, lines2):
    input_string = lines1
    reference_string = lines2
    
    m, n = len(input_string), len(reference_string)
    if m < n:
        input_string, reference_string = reference_string, input_string
        m, n = n, m
    d = [list(range(n + 1))] + [[i] + [0] * n for i in range(1, m + 1)]
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if input_string[i - 1] == reference_string[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1]) + 1
    distance = d[m][n]
    max_length = max(len(input_string), len(reference_string))
    similarity = 1 - (distance / max_length)
    return similarity

      
def get_all_files(directory):
    file_list = []

    for root, directories, files in os.walk(directory):
        for file in files:
            # Optimization: to lookup and compare only .java files (you can simply change it or disable it)
            # if ".java" in file:
            file_list.append(os.path.join(root, file))

    return file_list


# Start the timer
start_time = seconds=time.time()+7200
str_time = time.strftime('%H:%M:%S', time.gmtime(start_time))
print(f"START TIME: {str_time}")

# Get all files to compare
files_to_compare = get_all_files(root_folder)
files_num = len(files_to_compare)
num_files_to_compare = int(math.factorial(files_num) / (math.factorial(files_num-2) * 2))
print(f"FILES NUMBER {files_num} / {num_files_to_compare} reamining_to_compare \n")

# Global shared variables between threads
identical_groups = {}
group_id = 0
perc_info = {'num_files_to_compare': num_files_to_compare, 'comp_files_num': 0, 'old_perc': 0, 'start_time': start_time}

compare_files(files_num, start_time)


print(f"COMAPRED_FILES: {perc_info['comp_files_num']}")

# Print the groups of similar files
groups = {}
for file_path, group_id in identical_groups.items():
    if group_id not in groups:
        groups[group_id] = []
    groups[group_id].append(file_path)

# Open the output file in write mode
with open(output_file_path, 'w') as output_file:
    print("\n\nSimilar file groups:")
    output_file.write("\nSimilar file groups:\n\n")
    for group_id, files in groups.items():
        print(f"Group {group_id}:")
        output_file.write(f"Group {group_id}:\n")
        first = True
        for file_path in files:
            if first:
                # Don't delete original(first occured) file
                print(f"{file_path}")
                output_file.write(f"{file_path}\n")
                first = False
            else:
                # You should use separate script "delete_marked.py" for delete task
                # os.remove(file_path)
                print(f"{file_path} remove")
                output_file.write(f"{file_path} remove\n")
        print()
        output_file.write(f"\n")

# Stop the timer
end_time = time.time()+7200

# Calculate the execution time
execution_time = end_time - start_time
# Print the execution time
print()
str_time = time.strftime('%H:%M:%S', time.gmtime(execution_time))
print(f"Execution time: {str_time}")
