import pathlib
import re
import os

class DuplicatedFiles(Exception):
    def __init__(self, filename:str):
        self.filename = filename
        
    def __str__(self):
        return f"Duplicated Files Found: for file named {self.filename}"

class FileNotExist(Exception):
    def __init__(self, filename:str):
        self.filename = filename
        
    def __str__(self):
        return f"No File Found: for file named {self.filename}"

def redirect_absolute_dir(adir:str, root_dir:str) -> str:
    _, filename = os.path.split(adir)
    pl:pathlib.Path = pathlib.Path(root_dir)
    target_files = pl.rglob(filename)
    ori_path:list[pathlib.Path] = []
    src_file:pathlib.Path = pathlib.Path()
    for each in target_files:
        ori_path.append(each)
    if len(ori_path) == 1:
        src_file = ori_path[0]
    elif len(ori_path) == 0:
        raise FileNotExist(filename)
    else:
        raise DuplicatedFiles(filename)
    adir = str(src_file.absolute())
    return adir