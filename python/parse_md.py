# Parse the ../html folder year by year, month by month, day by day
# Create index.html files from the README.md and LIESMICH.md in these folders
# v25.10.02

import os, csv
import pandas as pd
from pathlib import Path

years  = []   # list of years  with events in "YYYY"  
months = []   # list of months with events in "YYYY/MM"
events = []   # list of dates  for  events in "YYYY/MM/DD"
m_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def list_subfolders(base_path):
    subfolders = []
    for root, dirs, files in os.walk(base_path):
        for d in dirs:
            folder_path = os.path.join(root, d)
            subfolders.append(os.path.relpath(folder_path, base_path))
    return subfolders

def check_folders(subfolders):
    global years, months, events
    total_number_folders = len(subfolders)
    print(f"Check validity of {total_number_folders} folders: ", end="")
    invalid_folders = []
    for index, folder in enumerate(subfolders):
        length = len(folder)
        if length == 4:
            years.append(folder)
        elif length == 7:
            months.append(folder)
        elif length == 10:
            events.append(folder)
        else:
            invalid_folders.append(folder)
    if len(invalid_folders) == 0:
        print("valid.")
        return True
    else:
        print(f"found {len(invalid_folders)} invalid folders.")
        for foldername in invalid_folders:
            print(foldername)
        print("*** Please fix his first ***")
        return False

def get_title_event(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        first_line = file.readline()
        if first_line.startswith('# '):
            return first_line.lstrip('# ').strip()
        return None    

def list_events(events):
    print(f"In total there are {len(events)} events:")
    for year in years:
        print(year)
        list_months = [m for m in months if m.startswith(year + "/")]
        for month in list_months:
            nr_month = int(month[-2:])
            print(f"  {m_names[nr_month - 1]}")
            list_events = [e for e in events if e.startswith(month + "/")]
            for event in list_events:
                date = event.replace("/", "-")
                df.loc[date] = [False, False, " ", " ", 0, 0, 0, 0]
                folder = Path(html_folder + "/" + event)
                print(f"    {event} ", end="")
                readme = folder / "README.md"
                liesmich = folder / "LIESMICH.md"
                has_readme = readme.is_file()
                has_liesmich = liesmich.is_file()
                if not has_readme and not has_liesmich:
                    print("❌ Neither README.md nor LIESMICH.md exist.")
                elif has_readme and not has_liesmich:
                    title_en = get_title_event(readme)
                    print(title_en)
                    df.loc[date, 'has_en'] = True
                    df.loc[date, 'title_en'] = title_en
                elif not has_readme and has_liesmich:
                    title_de = get_title_event(liesmich)
                    print(title_de)
                    df.loc[date, 'has_de'] = True
                    df.loc[date, 'title_de'] = title_de
                else: # in case of both
                    title_en = get_title_event(readme)
                    print(title_en)
                    df.loc[date, 'has_en'] = True
                    df.loc[date, 'title_en'] = title_en
                    print(f"    {event} ", end="")
                    title_de = get_title_event(liesmich)
                    print(title_de)
                    df.loc[date, 'has_de'] = True
                    df.loc[date, 'title_de'] = title_de

def export_to_csv(folder_list, output_file="folders.csv"):
    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Subfolder Path"])
        for folder in folder_list:
            writer.writerow([folder])

if __name__ == "__main__":
    html_folder = "../html"
    folders = list_subfolders(html_folder)
    column_titles = ['has_en', 'has_de', 'title_en', 'title_de', 'images', 'words_en', 'words_de', 'other_files']
    df = pd.DataFrame(columns=column_titles)
    # Convert the index to a datetime index (optional, but good practice for dates)
    df.index = pd.to_datetime(df.index)
    df.index.name = 'Date'
    df['has_en'] = df['has_en'].astype(bool)
    df['has_de'] = df['has_de'].astype(bool)

    if check_folders(folders):
        list_events(events)
    print(df)
    df.to_csv('list.csv')
    