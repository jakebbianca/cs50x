from cs50 import SQL
import sys


db = SQL("sqlite:///students.db")


def main():

    if len(sys.argv) != 2:
        print("Usage: python roster.py {house name}")
        exit(1)

    house = sys.argv[1]

    students = db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first", (house))

    for n in students:
        if n['middle'] != None:
            print(f"{n['first']} {n['middle']} {n['last']}, born {n['birth']}")
        else:
            print(f"{n['first']} {n['last']}, born {n['birth']}")


main()