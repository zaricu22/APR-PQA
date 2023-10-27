import os
import subprocess
import re

# Specify path to folder with separated projects by version (buggy, fixed, repaired)
work_folder = os.path.join('..', 'ManyBugs_Result')


for d in os.listdir(work_folder):
    if 'buggy' in d:
        buggy_folder = os.path.join(work_folder, d)
        buggy_file = os.path.join(buggy_folder, os.listdir(buggy_folder)[0])
        fixed_folder = buggy_folder.replace('buggy', 'fixed')
        fixed_file = os.path.join(fixed_folder, os.listdir(fixed_folder)[0])
        repaired_folder = buggy_folder.replace('buggy', 'repaired')
        repaired_file = os.path.join(repaired_folder, os.listdir(repaired_folder)[0])
        
        diff_fixed_command = 'diff '+"\""+buggy_file+"\" "+"\""+fixed_file+"\""
        diff_fixed_proc = subprocess.run(diff_fixed_command, shell=True, capture_output=True, text=True)
        out_fixed_proc = diff_fixed_proc.stdout
        add_num_fixed = 0
        for l in out_fixed_proc.splitlines():
            if l.startswith('>'):
                add_num_fixed += 1
        remove_num_fixed = 0
        for l in out_fixed_proc.splitlines():
            if l.startswith('<'):
                remove_num_fixed += 1
        chunks_num_fixed = len(re.findall(r"[0-9]+[a|d|c][0-9]+", out_fixed_proc))
        print(os.path.basename(fixed_folder)+" "+str(add_num_fixed)+" "+str(remove_num_fixed)+" "+str(chunks_num_fixed))

        diff_repaired_command = 'diff '+"\""+buggy_file+"\" "+"\""+repaired_file+"\""
        diff_repaired_proc = subprocess.run(diff_repaired_command, shell=True, capture_output=True, text=True)
        out_repaired_proc = diff_repaired_proc.stdout
        add_num_repaired = 0
        for l in out_repaired_proc.splitlines():
            if l.startswith('>'):
                add_num_repaired += 1
        remove_num_repaired = 0
        for l in out_repaired_proc.splitlines():
            if l.startswith('<'):
                remove_num_repaired += 1
        chunks_num_repaired = len(re.findall(r"[0-9]+[a|d|c][0-9]+", out_repaired_proc))
        print(os.path.basename(repaired_folder)+" "+str(add_num_repaired)+" "+str(remove_num_repaired)+" "+str(chunks_num_repaired))



