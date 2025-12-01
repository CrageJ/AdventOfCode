from pathlib import Path

def get_root_folder(child_folder="viz"): # gets the root folder by looking for a folder named viz
    curr = Path.cwd()
    while not (curr / child_folder).is_dir():
        curr = curr.parent
    return curr

def get_input(year,day,filename,split_whitespace=False):
    curr = get_root_folder()
    year = str(year)
    day = str(day)
    if not filename.endswith(".txt"):
        filename = filename + ".txt"
    curr = curr / year / day / filename
    with open(curr,'r') as file:
        data = file.readlines()
        data = [row.strip() for row in data]
        data = [row for row in data if row]

        if split_whitespace:
            data = [row.strip() for row in data]
        return data