"""
Parse nama lengkap menjadi nama depan dan nama belakang
Nama depan diambil dari kata pertama dari nama lengkap,
sedangkan nama belakang merupakan sisanya
"""

import csv, io, sys

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RELATIVE_DIR = BASE_DIR / 'csv'
RAW_FILENAME = sys.argv[1]
NIM = '13319'
LIMIT = 82

filename = RAW_FILENAME.split('.')[0] # File name without extension
in_file = open(RELATIVE_DIR / RAW_FILENAME, 'r') # Input file
out_file = open(RELATIVE_DIR / (filename + '_parsed.csv'), 'w') # Output file

data = in_file.read()
io_string = io.StringIO(data)
next(io_string)

out_file.write('username,first_name,last_name\n')

i = 0
for column in csv.reader(io_string):
    if i == LIMIT:
        break
    i += 1

    idx = column[0]
    if len(idx) == 1:
        nim = NIM + '00' + idx
    elif len(idx) == 2:
        nim = NIM + '0' + idx
    elif len(idx) == 3:
        nim = NIM + '' + idx

    first_name = column[1].split(' ')[0]
    last_name = ' '.join(column[1].split(' ')[1:])

    out_file.write(f'{nim},{first_name},{last_name}\n')

in_file.close()
out_file.close()
