import os
import subprocess
import re

i = 0
if __name__ == "__main__":
    # Specify full path to folder with separated projects by version (buggy, manual, auto)
    work_folder = os.path.join(os.getcwd(), '..', 'Bears_Result_32_Packages')
    out_file_path = 'Output-file-name (Bears).txt'

    with open(out_file_path, 'w') as file:
        for root, dirs, files in os.walk(work_folder):
            for f in files:
                file_path_cmp = os.path.join(root, f)
                tool_name = file_path_cmp.replace(work_folder, '').split(os.sep)[1]
                file_path_org = ""
                cmd = ""

                match = re.search(r"(_auto\s*\\|-auto\s*\\|_manual\s*\\|-manual\s*\\|_auto[-|_].*\\|-auto[-|_].*\\|_manual[-|_].*\\|-manual[-|_].*\\)", file_path_cmp, re.IGNORECASE)
                if match:
                    cmp_version = match.group(0)
                    prefix = cmp_version[0]
                    if(cmp_version[1] == cmp_version[1].upper()):
                        org_version = prefix+'Buggy'+'\\'
                    else:
                        org_version = prefix+'buggy'+'\\'                
                    file_path_org = file_path_cmp.replace(cmp_version, org_version)
                    if file_path_cmp.rstrip().endswith('.java') or file_path_cmp.rstrip().endswith('.c'): 
                        cmd = 'git diff --ignore-cr-at-eol --patch-with-raw'+" \""+file_path_org+"\" \""+file_path_cmp+"\""
                        p1 = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                        if p1.returncode == 1:
                            if 'Arja-Bears-dungba88-libra-436514153-436524727_0_Manual' in file_path_cmp:
                                print("DA")
                            i += 1
                            print(i)
                            file.write(str(i)+': '+cmp_version)
                            file.write('---'+p1.stdout.split('---')[1])

