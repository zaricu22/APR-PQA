import os
import shutil

# Enter the delete_file which contains marked paths to delete
delete_file = "Marked-dupliactes-all.txt"
marked_phrase = 'remove'

# Working folder to delete remaining empties
folder_path = 'D4J_Correct_80NoDupl (592Files)'

with open(delete_file, 'r') as file1:
    lines = file1.readlines()

# Extract lines with "marked_phrase"
removed_lines = [line for line in lines if marked_phrase in line]
print('NUM_FILES_TO_DELETE: '+str(len(removed_lines)))
print()

# Extract file paths from removed lines
file_paths = [line.split(' '+marked_phrase)[0] for line in removed_lines]

# Remove files
for file_path in file_paths:
    if os.path.exists(file_path):
        # Uncomment if you sure that content of provided "delete_file" are correct
        os.remove(file_path)
        print(f"Removed file: {file_path}")
    else:
        print(f"File not found: {file_path}")

# Delete empty folders
def delete_empty_folders(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)
            if not os.listdir(folder_path):  # Check if folder is empty
                os.rmdir(folder_path)
                print(f"Deleted empty folder: {folder_path}")
                
# Optimization: delete project folder if don't contains /src folder
def delete_folders_without_src(path):
    dirs = os.listdir(path)
    for d in dirs:
        folder_path = os.path.join(path, d)
        if not os.path.exists(os.path.join(folder_path,'src')):
            shutil.rmtree(folder_path)
            print(f"Deleted non-src folder: {folder_path}")

# Optimization: delete project folder if don't contains some of three version files
def delete_unavailable_version_folders(path):
    dirs = os.listdir(path)
    for d in dirs:
        curr_folder_path = os.path.join(path, d)
        d4j_project_version = d.split('-')[2]
        buggy_folder_path = curr_folder_path.replace(d4j_project_version,'Buggy')
        manual_folder_path = curr_folder_path.replace(d4j_project_version,'Manual')
        auto_folder_path = curr_folder_path.replace(d4j_project_version,'Auto')
        if os.path.exists(manual_folder_path):
            if os.path.exists(auto_folder_path):
                continue

        shutil.rmtree(buggy_folder_path, ignore_errors=True)
        shutil.rmtree(manual_folder_path, ignore_errors=True)
        shutil.rmtree(auto_folder_path, ignore_errors=True)
        print(f"Deleted non-manual/auto folder: {folder_path}")
        
        
print("\nDELETE EMPTY FOLDERS...\n")
delete_empty_folders(folder_path)
# delete_folders_without_src(folder_path)
# delete_unavailable_version_folders(folder_path)

