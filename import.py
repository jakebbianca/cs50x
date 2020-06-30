from cs50 import SQL
import sys
import csv


# need to initialize database as a sql item, as this will allow usage of sql queries in this program "db.execute("QUERY")
db = SQL("sqlite:///students.db")


def upload(reader):

    i = 0

    for n in reader:

        if n['name'].count(' ') == 1:
            a = n['name'].split(' ')[0]
            b = None
            c = n['name'].split(' ')[1]

        elif n['name'].count(' ') == 2:
            a = n['name'].split(' ')[0]
            b = n['name'].split(' ')[1]
            c = n['name'].split(' ')[2]

        db.execute("INSERT INTO students (id, first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?, ?)", (i, a, b, c, n['house'], n['birth']))

        i += 1


def main():

    # must accept a single command line argument after calling python file
    if len(sys.argv) != 2:
        print("Usage: python import.py CSVFILE")
        exit(1)

    # open csv file and create iterator
    f = open(sys.argv[1], newline='')
    reader = csv.DictReader(f, delimiter=',')

    upload(reader)


main()