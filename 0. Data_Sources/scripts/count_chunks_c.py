import os
import subprocess
import re

# Specify path to folder with separated projects by version (buggy, manual, auto)
work_folder = os.path.join('..', 'ManyBugs_Result')


for d in os.listdir(work_folder):
    if 'buggy' in d:
        buggy_folder = os.path.join(work_folder, d)
        buggy_file = os.path.join(buggy_folder, os.listdir(buggy_folder)[0])
        manual_folder = buggy_folder.replace('buggy', 'manual')
        manual_file = os.path.join(manual_folder, os.listdir(manual_folder)[0])
        auto_folder = buggy_folder.replace('buggy', 'auto')
        auto_file = os.path.join(auto_folder, os.listdir(auto_folder)[0])
        
        diff_manual_command = 'diff '+"\""+buggy_file+"\" "+"\""+manual_file+"\""
        diff_manual_proc = subprocess.run(diff_manual_command, shell=True, capture_output=True, text=True)
        out_manual_proc = diff_manual_proc.stdout
        add_num_manual = 0
        for l in out_manual_proc.splitlines():
            if l.startswith('>'):
                add_num_manual += 1
        remove_num_manual = 0
        for l in out_manual_proc.splitlines():
            if l.startswith('<'):
                remove_num_manual += 1
        chunks_num_manual = len(re.findall(r"[0-9]+[a|d|c][0-9]+", out_manual_proc))
        print(os.path.basename(manual_folder)+" "+str(add_num_manual)+" "+str(remove_num_manual)+" "+str(chunks_num_manual))

        diff_auto_command = 'diff '+"\""+buggy_file+"\" "+"\""+auto_file+"\""
        diff_auto_proc = subprocess.run(diff_auto_command, shell=True, capture_output=True, text=True)
        out_auto_proc = diff_auto_proc.stdout
        add_num_auto = 0
        for l in out_auto_proc.splitlines():
            if l.startswith('>'):
                add_num_auto += 1
        remove_num_auto = 0
        for l in out_auto_proc.splitlines():
            if l.startswith('<'):
                remove_num_auto += 1
        chunks_num_auto = len(re.findall(r"[0-9]+[a|d|c][0-9]+", out_auto_proc))
        print(os.path.basename(auto_folder)+" "+str(add_num_auto)+" "+str(remove_num_auto)+" "+str(chunks_num_auto))



