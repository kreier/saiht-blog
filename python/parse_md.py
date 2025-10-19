# Parse the ../html folder year by year, month by month, day by day
# Create index.html files from the README.md and LIESMICH.md in these folders
# v25.10.05

import os, csv
import pandas as pd
from pathlib import Path

years  = []   # list of years  with events in "YYYY"  
months = []   # list of months with events in "YYYY/MM"
events = []   # list of dates  for  events in "YYYY/MM/DD"
m_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
m_namen = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]

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
        years.sort()
        months.sort()
        events.sort()
        return True
    else:
        print(f"found {len(invalid_folders)} invalid folders.")
        for foldername in invalid_folders:
            print(foldername)
        print("*** Please fix his first ***")
        return False

def write_readme(path, content):
    # Define the output file name
    file_name = path / "README.md"
    try:
        # Open the file in write mode ('w'). 
        # Using 'utf-8' encoding is best practice for text files.
        with open(file_name, 'w', encoding='utf-8') as f:
            # Write the final combined string to the file
            f.write(content)
        # print(f"\n✅ Successfully exported markdown data to {file_name}")
    except IOError as e:
        print(f"\n❌ Error writing file: {e}")

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
            # All events for this month have been parsed - L3
            # Now lets create a L3 summary README.md for the month
            md_string = []
            md_string.append(f"# {m_names[nr_month - 1]} {year} ({len(list_events)})")
            md_string.append(" ")
            for event in list_events:
                date = event.replace("/", "-")
                if df.loc[date, 'has_en']:
                    title = df.loc[date, 'title_en']
                    md_string.append(f'### [{title}](./{event[-2:]})')
                    md_string.append(" ")
                    md_string.append(f"Here will be a short summary or the first paragraph of the event. Guess I have to figure this out. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. [Continue reading ...](./{event[-2:]})")
                    md_string.append(" ")
                if df.loc[date, 'has_de']:
                    title = df.loc[date, 'title_de']
                    md_string.append(f'### [{title}](./{event[-2:]})')
                    md_string.append(" ")
                    md_string.append(f"Here will be a short summary or the first paragraph of the event. Guess I have to figure this out. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. [Continue reading ...](./{event[-2:]})")
                    md_string.append(" ")                    
            md_string = "\n".join(md_string)
            write_readme(Path(html_folder + "/" + month), md_string)
        # L2 for all events of the year
        # First, fix the index of the dataframe
        df.index = pd.to_datetime(df.index, errors='coerce')
        md_string = []
        md_string.append(f"# Events {year} ({len(list_events)})")
        md_string.append(" ")
        for month in list_months:
            nr_month = int(month[-2:])
            target_month = month.replace("/", "-")
            df_target = df.loc[target_month]
            md_string.append(f"## [{m_names[nr_month - 1]}](./{month[-2:]}) ({len(df_target)})")
            md_string.append(" ")
            # no need to parse, the titles are already in the df
            df_target = df.loc[target_month]
            for date_key, row in df_target.iterrows():
                str_mmdd = date_key.strftime('%m/%d')
                if row['has_en']:
                    md_string.append(f"- **{date_key.strftime('%Y-%m-%d')}** [{row['title_en']}](./{str_mmdd})")
                    md_string.append(" ")
                if row['has_de']:
                    md_string.append(f"- **{date_key.strftime('%Y-%m-%d')}** [{row['title_de']}](./{str_mmdd})")
                    md_string.append(" ")
        md_string = "\n".join(md_string)
        write_readme(Path(html_folder + "/" + year), md_string)
    # Just the L1 is left - an updated README.md in the /html folder for Github
    md_string = []
    md_string.append(f"# Blog on saiht.de")
    md_string.append(" ")
    for year in years:
        df_target = df.loc[year]
        md_string.append(f"## {year} ({len(df_target)})")
        md_string.append(" ")
        for date_key, row in df_target.iterrows():
            str_yyyymmdd = date_key.strftime('%Y/%m/%d')
            if row['has_en']:
                md_string.append(f"- **{date_key.strftime('%Y-%m-%d')}** [{row['title_en']}](./{str_yyyymmdd})")
                md_string.append(" ")
            if row['has_de']:
                md_string.append(f"- **{date_key.strftime('%Y-%m-%d')}** [{row['title_de']}](./{str_yyyymmdd})")
                md_string.append(" ")
    md_string = "\n".join(md_string)
    write_readme(Path(html_folder), md_string)
                                     
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
    # print(df)
    df.to_csv('list.csv')
    