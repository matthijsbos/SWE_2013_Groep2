import unittest
from os import name, path, rename, getcwd

if __name__ == '__main__':
    directory_separator = ('/' if name == "posix" else '\\')
    src = path.abspath(path.join(getcwd(), path.pardir))+directory_separator+"db.sqlite"
    dst = path.abspath(path.join(getcwd(), path.pardir))+directory_separator+"db_backup.sqlite"
    rename(src, dst)
