import subprocess
import csv
import re
import os
from datetime import datetime
import argparse
from pathlib import Path

def export_git_flag_logs(export_filename: str="git_status_logs.csv", folders_to_check: str="", sort_by: str="", filter_status: str="", 
                         include_timestamp: bool=True, strip_prefix: bool=True, filter_extensions: str="") -> None:
    """
    Export the logs from the 'git status' command for the 'iso3166-flag-icons' 
    repo that outlines all the changes made to the repo, including additions, 
    changes and deletions to the flag folders. Mainly created for testing &
    to keep an accurate and readable log for big changes made to the repo. 

    Parameters
    ==========
    :export_filename: str (default="git_status_logs.csv")
        filename for export file.
    :folders_to_check: str (default="")
        1 or more specific directories to get the change logs for.
    :sort_by: str (default="status")
        attribute in export file to sort_by, by deafult the rows will 
        be sorted by the status attribute.
    :filter_status: str (default="")
        filter the status column, only including those files that have
        been "added", "modified" or "deleted". By default all of these
        status files will be included.
    :include_timestamp: (default=True)
        whether to include the timestamp attribute per file row. The
        timestamp functionality can take up a lot of time to generate.
    :strip_prefix: bool (default=True)
        whether to remove the relative folder prefix from the flag files
        e.g remove "../" from the paths.
    :filter_extensions: str (default="md")
        exclude a specific list of files from the output file via their 
        extensions, e.g to exclude markdown files, pass in ".md".

    Returns
    =======
    None

    Raises
    ======
    OSError:
        Input folders in folders_to_check parameter do not exist.
    """
    #run git status command using subprocess and get the full output
    result = subprocess.run(["git", "status"], stdout=subprocess.PIPE, text=True)
    lines = result.stdout.splitlines()

    #vars to track the specific changes
    section = None
    modified = []
    deleted = []
    added = []

    #returning the logs for a specific subset of folders in the repo
    if folders_to_check:
        #split string into a list and strip spaces
        folder_list = [f.strip() for f in folders_to_check.split(',') if f.strip()]

        #validate all folders input into parameter are valid, raise OSError if not
        missing_folders = [folder for folder in folder_list if not os.path.isdir(folder)]
        if missing_folders:
            raise OSError(f"The following folder(s) do not exist: {', '.join(missing_folders)}.")

        #regex that accepts optional ./ or ../ prefix before folder
        escaped_folders = [re.escape(folder) for folder in folder_list]
        folder_pattern = r'^(\.\.?/)?(' + '|'.join(escaped_folders) + r')/'
        folder_regex = re.compile(folder_pattern)
    else:
        #default regex if no folder is passed - defaults to searchinf over the iso3166-1 & iso3166-2 icon folders
        folder_regex = re.compile(r'^(\.\.?/)?iso3166-[12]-icons/')

    #list of all changes
    change_log = []

    #iterate over each line in output of git status command
    for line in lines:
        line = line.strip()

        #headers in git status output
        if "Changes not staged for commit:" in line:
            section = "not_staged"
            continue
        elif "Untracked files:" in line:
            section = "untracked"
            continue
        elif not line or line.startswith("("):
            #skip empty lines and hints like "(use 'git add'...)"
            continue

        #process files based on section - not-staged & untracked
        if section == "not_staged":
            if line.startswith("modified:") or line.startswith("deleted:"):
                #extract status and path from lines
                status, path = line.split(":", 1)
                path = path.strip()
                original_path = path
                if folder_regex.match(path):
                    #get timestamp for committed file
                    timestamp = get_git_timestamp(original_path) if include_timestamp else ""
                    #remove prefix from folders e.g remove "../"
                    if strip_prefix:
                        path = re.sub(r'^(\.\.?/)+', '', path)
                    #extact the individual file info given a full path - name folder & extension, append relevant attriubutes & data to change log list
                    folder, filename, extension = extract_file_metadata(path)                    
                    change_log.append([path, status.strip(), timestamp, folder, filename, extension])

        #parse untracked files list that haven't been added from local to git repo
        elif section == "untracked":
            path = line.strip()
            if folder_regex.match(path):
                #for untracked files, there is no commit timestamp so try and parse timestamp from local machine
                timestamp = get_filesystem_timestamp(path) if include_timestamp else ""
                #extact the individual file info given a full path - name folder & extension, append to change log list
                folder, filename, extension = extract_file_metadata(path)
                #remove prefix from folders e.g remove "../"
                if strip_prefix:
                    path = re.sub(r'^(\.\.?/)+', '', path)
                #append relevant attriubutes & data to change log list 
                change_log.append([path, "added", timestamp, folder, filename, extension])

    #set all lists to the same length
    max_len = max(len(modified), len(added), len(deleted))
    modified += [''] * (max_len - len(modified))
    added += [''] * (max_len - len(added))
    deleted += [''] * (max_len - len(deleted))

    #filter by commit status, accepted values are 'added', 'modified' or 'deleted'
    if filter_status:
        if isinstance(filter_status, str):
            filter_status = [s.strip() for s in filter_status.split(',') if s.strip()]
        valid_statuses = set(s.lower() for s in filter_status)
        change_log = [row for row in change_log if row[1].lower() in valid_statuses]
    
    #by default the rows will be sorted by the "status" attribute, but the output can be sorted via the other columns
    if sort_by == "status":
        #sort status into desired order
        status_order = {'added': 0, 'modified': 1, 'deleted': 2}
        change_log.sort(key=lambda row: status_order.get(row[1], 99))
    elif sort_by == "timestamp":
        change_log.sort(key=lambda row: row[2] or "")
    elif sort_by == "filename":
        change_log.sort(key=lambda row: row[4].lower())  # filename is column 4
    elif sort_by == "folder":
        change_log.sort(key=lambda row: row[3].lower())  # folder is column 3
    elif sort_by == "extension":
        change_log.sort(key=lambda row: row[5].lower())  # folder is column 3

    #exclude specific files in the output file by inputting their extension e.g to exclude markdown files input "md" 
    if filter_extensions:
        if isinstance(filter_extensions, str):
            filter_extensions = [ext.strip().lstrip('.').lower() for ext in filter_extensions.split(',') if ext.strip()]
        else:
            filter_extensions = [ext.lower().lstrip('.') for ext in filter_extensions]
        #update change log with filtered out files
        change_log = [row for row in change_log if row[5].lower() not in filter_extensions]

    #export to CSV
    with open(export_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['file', 'status', 'timestamp', 'folder', 'filename', 'extension', 'notes'])
        for row in change_log:
            writer.writerow(row + [""]) #optional notes column added to each row

    print(f"CSV written to {export_filename}.")

def get_git_timestamp(file_path: str, status: str="") -> str:
    """
    Return last Git commit timestamp or 'not-committed' for uncommitted modified/deleted files.
    
    Parameters
    =========
    :file_path: str
        path to file to get the change timestamp for.
    :status: str (default="")
        status of file change - added, modified or deleted.

    Returns
    =======
    :timestamp: str
        timestamp in the form Mon 8th Aug 22:30. If the timestamp 
        can't be captured then an empty string will be returned.
    """
    try:
        #use subprocess library and the git log command to get the timestamp of the file changes
        result = subprocess.run(
            ["git", "log", "-1", "--date=iso-local", "--format=%ad", "--", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        #parse the timestamp from the output, removign any excess whitespace
        raw_timestamp = result.stdout.strip()

        #return committed or non-commited timestamp if applicable
        if not raw_timestamp:
            if status.lower() in ("modified", "deleted"):
                return "not-committed"
            else:
                #for untracked files (e.g., added), fallback to filesystem timestamp 
                return get_filesystem_timestamp(file_path)

        #get timestamp in correct format via the datetime library 
        dt = datetime.strptime(raw_timestamp, "%Y-%m-%d %H:%M:%S")
        weekday = dt.strftime('%a') + 's'
        day = dt.day
        suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

        return f"{weekday} {day}{suffix} {dt.strftime('%B %Y %H:%M')}"

    #return empty string if issue parsing the timestamp
    except Exception as e:
        return ""

def get_filesystem_timestamp(file_path: str) -> str:
    """ 
    Return filesystem-modified timestamp for input filename formatted as 'Tues 15th July 2025 17:54'.
    
    Parameters
    ========== 
    :file_path: str
        path to file to get the change timestamp for.

    Returns
    =======
    :formatted_date: str
        formatted timestamp for file change.
    """
    try:
        #parse modification timestamp
        mod_time = os.path.getmtime(file_path)
        dt = datetime.fromtimestamp(mod_time)

        #get timestamp in correct format via the datetime library 
        weekday = dt.strftime('%a') + 's'  # 'Tue' -> 'Tues'
        day = dt.day
        suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
        formatted_date = f"{weekday} {day}{suffix} {dt.strftime('%B %Y %H:%M')}"

        return formatted_date

    #return empty string if issue parsing the timestamp
    except Exception:
        return ""
    
def extract_file_metadata(path: str) -> tuple[str, str, str]:
    """
    Given a relative or prefixed file path (e.g., ../iso3166-1-icons/ad.svg),
    return (folder, filename, extension).

    Parameters
    ==========
    :file_path: str
        path to file to get the change timestamp for.

    Returns
    =======
    :folder: str
        folder name.
    :filename: str
        filename.
    :extension: str
        filename extension.

    Raises
    ======
    OSError:
        File path doesn't exist.
    """
    #raise error if file path doesnt exist
    if not (os.path.isfile(path)):
        raise OSError(f"Filepath not found: {path}.")
    
    #parse filename, extension and folder from input file path
    folder = Path(path).parts[-2] if len(Path(path).parts) >= 2 else ""
    filename = os.path.basename(path)
    extension = os.path.splitext(filename)[1].lstrip(".").upper()

    return folder, filename, extension

if __name__ == '__main__':

    #parse input arguments using ArgParse 
    parser = argparse.ArgumentParser(description='Script for exporting the logs from the git status command.')

    parser.add_argument('-export_filename', '--export_filename', type=str, required=False, default="git_status_logs.csv", 
        help='Export filename for git status logs.')
    parser.add_argument('-folders_to_check', '--folders_to_check', type=str, required=False, default="", 
        help='1 or more directories to get the specific log data for.')
    parser.add_argument('-sort_by', '--sort_by', type=str, required=False, default="status", 
        help='Attribute in export file to sort_by, by deafult the rows will be sorted by the status attribute.')
    parser.add_argument('-filter_status', '--filter_status', type=str, required=False, default="", 
        help='Filter the status column, only including those files that have been "added", "modified" or "deleted.')
    parser.add_argument('-include_timestamp', '--include_timestamp', required=False, action=argparse.BooleanOptionalAction, default=1, 
        help='Whether to include the timestamp attribute per file row. The timestamp functionality can take up a lot of time to generate.')
    parser.add_argument('-strip_prefix', '--strip_prefix', required=False, action=argparse.BooleanOptionalAction, default=0, 
        help='Whether to remove the relative folder prefix from the flag files e.g remove "../" from the paths.')
    parser.add_argument('-filter_extensions', '--filter_extensions', type=str, required=False, default="", 
        help='Exclude a specific list of files from the output file via their extensions, e.g to exclude markdown files, pass in "md".')

    #parse input args
    args = parser.parse_args()
    
    #create output file for git status command
    export_git_flag_logs(**vars(args))