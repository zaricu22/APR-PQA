import os
import subprocess
import json
import re

# Specify full path to folder with separated projects by version (buggy, fixed, repaired)
work_folder = os.path.join(os.getcwd(), '..', 'Bugs.jar_Result_51_Packages')
out_file_path = 'Output-file-name (Bugs.jar).json'

results = []

for root, dirs, files in os.walk(work_folder):
    for f in files:
        file_path_cmp = os.path.join(root, f)
        file_path_org = ""
        if ('Repaired' in file_path_cmp or 'Fixed' in file_path_cmp) and '.java' in file_path_cmp:
            if 'Repaired' in file_path_cmp:
                file_path_org = file_path_cmp.replace('Repaired', 'Buggy')
            if 'Fixed' in file_path_cmp:
                file_path_org = file_path_cmp.replace('Fixed', 'Buggy')
            cmd = 'git diff --patch-with-raw'+" \""+file_path_org+"\" \""+file_path_cmp+"\""
            p1 = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if p1.returncode == 1:
##                print(p1.stdout)
##                print()
                diff_content_lines = p1.stdout.split('\n')
                total_add = 0
                total_rm = 0
                total_lines = 0
                local_chunk_add = 0
                local_chunk_rm = 0
                chunk_count = 0
                local_chunks = []
                new_chunk = False
                for l in diff_content_lines:
                    if (l.startswith('-') and not l.startswith('--')) or (l.startswith('+') and not l.startswith('++')):
                        if not new_chunk: 
                            chunk_count = chunk_count + 1
                            local_chunk_add = 0
                            local_chunk_rm = 0
                            # print(str(new_chunk)+"  "+repr(l))
                        new_chunk = True
                        if l.startswith('+'):
                            local_chunk_add += 1
                            total_add += 1
                        if l.startswith('-'):
                            local_chunk_rm += 1
                            total_rm += 1
                    else:
                        if(new_chunk):
                            if(local_chunk_add > 0 and local_chunk_rm > 0):
                                total_lines += min(local_chunk_add, local_chunk_rm)+abs(local_chunk_add - local_chunk_rm)
                            else:
                                total_lines += abs(local_chunk_add - local_chunk_rm)
                        new_chunk = False
                            
                tool_name = file_path_cmp.replace(work_folder, '').split(os.sep)[1]
                results.append({'name': tool_name, 'chunk_num': chunk_count, 'add': total_add, 'rm': total_rm, 'lines': total_lines})
            else:
                tool_name = file_path_cmp.replace(work_folder, '').split(os.sep)[1]
                results.append({'name': tool_name, 'chunk_num': 0, 'add': 0, 'rm': 0, 'lines': 0})

print(str(len(results)))

with open(out_file_path, 'w') as file:
    file.write(json.dumps(results, indent=2))

