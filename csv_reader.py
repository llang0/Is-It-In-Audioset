# load audioset into a sqlite file
# usage: python csv_reader.py <filename> <database>
# .schema "# YTID" TEXT, " start_seconds" TEXT, " end_seconds" TEXT, " positive_labels" TEXT);

import sys
import sqlite3
import csv
import argparse

parser = argparse.ArgumentParser(
    description="Load audioset data into sqlite using python.", 
    usage="python csv_reader.py <csv file> <database file>"
    )

parser.add_argument('filename')
parser.add_argument('database')
parser.add_argument('-pids', '--positive-ids', action='store_true')
args = parser.parse_args()

filename = args.filename
database = args.database



def read_csv():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {filename.split('.')[0]} (
                YTID TEXT PRIMARY KEY,
                start_seconds TEXT,
                end_seconds TEXT
    );''')

    with open(filename) as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            columns = row[:3]
            # while len(columns) > 3:
            #     columns.

            cursor.execute(f'''INSERT INTO {filename.split('.')[0]} (YTID, start_seconds, end_seconds) VALUES (?, ?, ?);''', columns)
            print(columns)

    conn.commit()
    conn.close()
    print(f"{filename} - {database}")

def read_pids():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS positive_labels (
                   id INTEGER PRIMARY KEY,
                   YTID TEXT,
                   positive_label TEXT
    );''')

    with open(filename) as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            while len(row) > 3:
                pid = row.pop()
                pid = pid.replace('"', '')
                pid = pid.replace(' ', '')
                print(f"{row[0]} - {pid}")
                cursor.execute('''INSERT INTO positive_labels (YTID, positive_label) VALUES (?, ?);''', (row[0], pid))

    conn.commit()
    conn.close()
    print(f"{filename} - {database} - positive labels")
    


def main():
    if args.positive_ids:
        read_pids()
    else:
        read_csv()

if __name__ == "__main__":
    main()
