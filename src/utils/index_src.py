"""_summary_ index symbols in source code ans store them in a sqlite3 database.
"""

from clang.cindex import *
import sqlite3
import os
import pathlib
from . import log

TARGET_DATABASE = "index.sqlite"

Config.set_library_path("/Library/Developer/CommandLineTools/usr/lib")

class SymbolType:
    Function = "function"
    Class = "class"
    Struct = "struct"
    Enum = "enum"
    Union = "union"
    Method = "method"
    Constructor = "constructor"
    Destructor = "destructor"

def init_db():
    """
    Initializes the database by creating the necessary table if it doesn't exist.

    This function checks if the target database file already exists. If it does, it prompts the user for confirmation
    before overwriting the existing database. If the user confirms, the existing database is deleted and a new one is
    created. After connecting to the database, it creates the 'index_src' table if it doesn't already exist.

    Returns:
        None
    """
    if os.path.exists(TARGET_DATABASE):
        log.warning(f"Database {TARGET_DATABASE} already exists. This will overwrite the existing database. Continue? (Y/[n])")
        user_choice = input()
        if user_choice.lower() != "y":
            log.fatal("Program terminated by user.")
            exit(0)
        os.remove(TARGET_DATABASE)
    conn = sqlite3.connect(TARGET_DATABASE)
    if conn is None:
        log.fatal("Cannot connect to database.")
        exit(1)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS index_src
                 (id INTEGER PRIMARY KEY, name TEXT, type TEXT, file TEXT, line INTEGER)''')
    conn.commit()
    conn.close()


def index_src_file(file_path: str):
    """
    Indexes the source file specified by the given file path.

    Parameters:
        file_path (str): The path to the source file to be indexed.

    Returns:
        None

    Raises:
        None
    """
    index = Index.create()
    tu = index.parse(file_path)
    conn = sqlite3.connect(TARGET_DATABASE)
    c = conn.cursor()
    SQL_PATTERN = "INSERT INTO index_src (name, type, file, line) VALUES (?, ?, ?, ?)"
    for i in tu.cursor.get_tokens():
        if i.kind == TokenKind.IDENTIFIER:
            if i.cursor.kind == CursorKind.FUNCTION_DECL:
                c.execute(SQL_PATTERN,
                          (i.spelling, SymbolType.Function, f"{file_path}", i.cursor.location.line))
            elif i.cursor.kind == CursorKind.CLASS_DECL:
                c.execute(SQL_PATTERN,
                          (i.spelling, SymbolType.Class, f"{file_path}", i.cursor.location.line))
            elif i.cursor.kind == CursorKind.STRUCT_DECL:
                c.execute(SQL_PATTERN,
                          (i.spelling, SymbolType.Struct, f"{file_path}", i.cursor.location.line))
            elif i.cursor.kind == CursorKind.ENUM_DECL:
                c.execute(SQL_PATTERN,
                          (i.spelling, SymbolType.Enum, f"{file_path}", i.cursor.location.line))
            elif i.cursor.kind == CursorKind.UNION_DECL:
                c.execute(SQL_PATTERN,
                          (i.spelling, SymbolType.Union, f"{file_path}", i.cursor.location.line))
            elif i.cursor.kind == CursorKind.CXX_METHOD:
                c.execute(SQL_PATTERN,
                          (i.spelling, SymbolType.Method, f"{file_path}", i.cursor.location.line))
            elif i.cursor.kind == CursorKind.CONSTRUCTOR:
                c.execute(SQL_PATTERN,
                          (i.spelling, SymbolType.Constructor, f"{file_path}", i.cursor.location.line))
            elif i.cursor.kind == CursorKind.DESTRUCTOR:
                c.execute(SQL_PATTERN,
                          (i.spelling, SymbolType.Destructor, f"{file_path}", i.cursor.location.line))
            else:
                continue
            log.success(f"Found identifier \033[34m{i.spelling}\033[0m of type \033[36m{i.cursor.kind}\033[0m at \033[33m{file_path}:{i.cursor.location.line}\033[0m")
    conn.commit()
    conn.close()


def index_dir(dir_path:str):
    pass