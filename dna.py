import csv
import sys


def STR_chain_counter(STR, STRlen, c0, DNAfile, streak):
    if STR == DNAfile[c0:c0 + STRlen]:
        c1 = c0 + STRlen
        streak += 1
        k = STR_chain_counter(STR, STRlen, c1, DNAfile, streak)
        return k
    else:
        return streak


# open the given csv file and read to memory
csvfile = open(sys.argv[1], newline = '')
csvread = csv.reader(csvfile, delimiter = ',')
# this 'next' allows me to easily access the first conceptual row
headers = next(csvread)
headercount = len(headers)
csvfile.seek(0)
rowcount = sum(1 for row in csvread)

# open the given text file and read to memory
# the open() function assumes 'r' as the second argument if omitted, so this is opening to read
txtfile = open(sys.argv[2])
txt = txtfile.read()
txtlen = len(txt)

# create a new list series to align the given STRs with count variables
nSTR = headers, [0 for n0 in range(headercount)]

# create a list series to assign a max consecutive STR count to each character in the DNA txt
# CURRENTLY UNUSED
nDNA = txt, [0 for n1 in range(txtlen)]

# iterate through STR, keeping track of the longest consecutive count that can be found
for i in range(1, headercount):
    STR = nSTR[0][i]
    STRlen = len(STR)
    m = 0
    streak = 0

    for j in range(0, txtlen):
        k = STR_chain_counter(STR, STRlen, j, txt, streak)
        if m < k:
            m = k

    nSTR[1][i] = m

# return to top of file and use next() to get to 2nd line (not sure yet if there is a better way)
csvfile.seek(0)
headers = next(csvread)

for a in range(1, rowcount):
    # can i repeatedly "next()" to load each row / each person's name and STR counts to check against nSTR?
    personSTR = next(csvread)
    for b in range(1, headercount):
        # the below doesn't work without casting to ints; seems to be due to nSTR being a tuple and personSTR being a list, as comparison is intentionally not supported
        if int(nSTR[1][b]) == int(personSTR[b]):
            if b == headercount - 1:
                print(personSTR[0])
                exit(0)
            else:
                continue
        else:
            break

print("No match")