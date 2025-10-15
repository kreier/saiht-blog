# Parse the ../html folder year by year, month by month, day by day
# Create index.html files from the README.md and LIESMICH.md in these folders
# v25.10.01


import os
import csv

def list_subfolders(base_path="../html"):
    subfolders = []
    for root, dirs, files in os.walk(base_path):
        for d in dirs:
            folder_path = os.path.join(root, d)
            subfolders.append(os.path.relpath(folder_path, base_path))
    return subfolders

def export_to_csv(folder_list, output_file="folders.csv"):
    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Subfolder Path"])
        for folder in folder_list:
            writer.writerow([folder])

if __name__ == "__main__":
    html_folder = "../html"
    folders = list_subfolders(html_folder)
    export_to_csv(folders)
    print(f"✅ Found {len(folders)} folders. List saved to folders.csv")
