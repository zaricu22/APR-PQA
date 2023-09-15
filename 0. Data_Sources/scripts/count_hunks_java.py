import os
import subprocess
import json
import re

# Specify full path to folder with separated projects by version (buggy, fixed, repaired)
work_folder = os.path.join(os.getcwd(), '..', 'Defects4J_Tool_Result_220_Packages')
out_file_path = 'Bears_hunk-results_short.json'

results = []

for root, dirs, files in os.walk(work_folder):
    for f in files:
        file_path_org = os.path.join(root, f)
        file_path_cmp = ""
        if ('Repaired' in file_path_org or 'Fixed' in file_path_org) and '.java' in file_path_org:
            if 'Repaired' in file_path_org:
                file_path_cmp = file_path_org.replace('Repaired', 'Buggy')
            if 'Fixed' in file_path_org:
                file_path_cmp = file_path_org.replace('Fixed', 'Buggy')
            cmd = 'git diff --patch-with-raw'+" \""+file_path_org+"\" \""+file_path_cmp+"\""
            p1 = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if p1.returncode == 1:
                diff_content_lines = p1.stdout.split('\n')
                add = 0
                rm = 0
                hunk_count = 0
                new_hunk = False
                for l in diff_content_lines:
                    if (l.startswith('-') and not l.startswith('--')) or (l.startswith('+') and not l.startswith('++')):
                        if not new_hunk: 
                            hunk_count = hunk_count + 1
                            # print(str(new_hunk)+"  "+repr(l))
                        new_hunk = True
                        if l.startswith('+'):
                            add += 1
                        if l.startswith('-'):
                            rm += 1
                    else:
                        new_hunk = False
                tool_name = file_path_org.replace(work_folder, '').split(os.sep)[1]
                results.append({'name': tool_name, 'hunk_num': hunk_count, 'add': add, 'rm': rm})
            else:
                tool_name = file_path_org.replace(work_folder, '').split(os.sep)[1]
                results.append({'name': tool_name, 'hunk_num': 0, 'add': 0, 'rm': 0})

print(str(len(results)))

with open(out_file_path, 'w') as file:
    file.write(json.dumps(results, indent=2))

