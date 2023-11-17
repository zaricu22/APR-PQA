import os
import subprocess
import json
import re

chunk_count = 0
total_added = 0
total_removed = 0
total_updated = 0
total_moved = 0
total_lines = 0

def get_edited_lines(diff_content_lines):
    global total_added, total_removed, chunk_count
    
    chunks_edits_list = []
    chunk_add = 0
    chunk_rm = 0
    chunks = []
    new_chunk = False
    
    for l in diff_content_lines:
        if (l.startswith('-') and not l.startswith('--')) or (l.startswith('+') and not l.startswith('++')):
            if not new_chunk: 
                chunk_count = chunk_count + 1
                chunk_add = 0
                chunk_rm = 0
            new_chunk = True
            if l.startswith('+'):
##                if l[1:].rstrip(): # escape empty_lines
                    chunk_add += 1
                    total_added += 1
            elif l.startswith('-'):
##                if l[1:].rstrip(): # escape empty_lines
                    chunk_rm += 1
                    total_removed += 1
            chunks_edits_list.append(l)
        else:
            if new_chunk:
                chunks_edits_list.append('new_chunk')
            new_chunk = False

    return chunks_edits_list

def update_ops_check(edited_lines):
    global total_added, total_removed, total_updated, total_lines
    
    # all updated lines separated by chunks
    updated_lines_in_chunks = []
    updated_lines = []
    total_added_count = 0
    added_count = 0
    removed_count = 0
    curr_update_list_index = 0
    for cmp_el in edited_lines:
        if(cmp_el == 'new_chunk'):
            # deattach many deletions which are not part of updated lines
            if(removed_count > 0):
                start_index_of_update_section = removed_count
                updated_lines = updated_lines[start_index_of_update_section:]
            if(updated_lines and len(updated_lines) % 2 == 0):
                updated_lines_in_chunks.append(updated_lines)
            updated_lines = []
            added_count = 0
            removed_count = 0
        elif(cmp_el.startswith('+') and removed_count > 0):
            added_count += 1
            removed_count -= 1
            updated_lines.append(cmp_el)
            
            is_pos_line_empty = cmp_el[1:].rstrip()
            if is_pos_line_empty: 
                total_added_count += 1
                total_removed -= 1
            else:
                total_added -= 1
                # update with empty line is remove operation
                # but only if it is not part of move operation
                curr_pos = len(updated_lines) - 1
                neg_cp_index = curr_pos - (2 * added_count) + 1
                neg_counterpart = updated_lines[neg_cp_index]
                neg_cp_op_line = neg_counterpart[1:].strip()
                for curr_el in edited_lines:
                    if(curr_el.startswith('+') and neg_cp_op_line == curr_el[1:].strip()):
                        total_removed -= 1
                        total_lines += 1
                        break
        elif(cmp_el.startswith('-')):
            removed_count += 1
            updated_lines.append(cmp_el)
        # cover special case of updating existing with empty line
        elif(cmp_el.startswith('+') and not cmp_el[1:].rstrip()):
            total_added -= 1
    total_updated = total_added_count
    total_added -= total_updated
    total_lines += total_added + total_removed + total_updated
            
##    for l in edited_lines:
##        print(l)
##    print(updated_lines_in_chunks)

    return updated_lines_in_chunks

def move_ops_check(edited_lines, updated_lines_in_chunks):
    global total_added, total_removed, total_moved
    
    moved_lines_dict = {}
    for el in edited_lines:
        if el.startswith('-') and el[1:].rstrip(): # escape empty_lines
            inverse_op_line = el.rstrip().replace('-','+',1)
            op_line = el[1:].strip()
            count_inverse = 0

            # limit to exact number of moved lines,
            # the rest of lines are added or removed
            if(el not in moved_lines_dict.keys()):
                for cmp_el in edited_lines:
                    if(cmp_el.startswith('+') and op_line == cmp_el[1:].strip()):
                        count_inverse += 1
                moved_lines_dict[el] = count_inverse
            
            if moved_lines_dict[el] > 0:
                total_moved += 1
                moved_lines_dict[el] -= 1

                # move is not part of add or remove operations
                # copied lines are mentioned as add operation
                # check if moved lines is not part of updated lines
                pos_move_side_updated = False
                neg_move_side_updated = False
                for updated_lines in updated_lines_in_chunks:
                    for up_line in updated_lines:
                        if((up_line.startswith('+') or up_line.startswith('-')) and op_line in up_line[1:].strip()):
                            if(up_line.startswith('+')):
                                pos_move_side_updated = True
                            elif(up_line.startswith('-')):
                                neg_move_side_updated = True
                # decrement only if positive or negative side of move is not part of update,
                # otherwise it was decremented in update calculations
                if not pos_move_side_updated:
                    total_added -= 1
                if not neg_move_side_updated:
                    total_removed -= 1
                
def process_diff(diff_format):
    global total_added, total_removed, total_updated, total_moved, total_lines, chunk_count

    chunk_count = 0
    total_added = 0
    total_removed = 0
    total_updated = 0
    total_moved = 0
    total_lines = 0
                    
##    print(diff_format)
##    print()
    diff_content_lines = diff_format.split('\n')
    
    edited_lines = get_edited_lines(diff_content_lines)

    updated_lines_in_chunks = update_ops_check(edited_lines)

    move_ops_check(edited_lines, updated_lines_in_chunks)
    
##    print(f"add:{total_added}, remove:{total_removed}, update:{total_updated}, move:{total_moved}")
##    print(f"chunks:{chunk_count}, lines:{total_lines}")

    return f"{total_added} {total_removed} {total_updated} {total_moved} {chunk_count} {total_lines}"
        

if __name__ == "__main__":
    # Specify full path to folder with separated projects by version (buggy, manual, auto)
    work_folder = os.path.join(os.getcwd(), '..', 'ManyBugs_Result_19_VCXProjects')
    out_file_path = 'Output-file-name (ManyBugs).json'

    final_results = []
    i = 0
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
                        process_diff(p1.stdout)
                        final_results.append({'name': tool_name, 'add': total_added, 'rm': total_removed, 'upd': total_updated, 'mv': total_moved, 'chunk_num': chunk_count, 'lines': total_lines})
                    else:
                        final_results.append({'name': tool_name, 'add': 0, 'rm': 0, 'upd': 0, 'mv': 0, 'chunk_num': 0, 'lines': 0, })

    print(str(len(final_results)))

    with open(out_file_path, 'w') as file:
        file.write(json.dumps(final_results, indent=2))     
    

