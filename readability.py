from cs50 import get_string


s = get_string("Text: ")

l = list(s)

length = len(l)
i = 0

lcount = 0
wcount = 0
scount = 0

while i < length:
    if l[i].isalpha() == True:
        lcount += 1
    elif l[i].isspace() == True:
        wcount += 1
    elif "!" in l[i] or "." in l[i] or "?" in l[i]:
        scount += 1
    i += 1

if "!" in l[length - 1] or "." in l[length - 1] or "?" in l[length - 1]:
    wcount += 1


# letters per 100 words
L = lcount / wcount * 100

# how many sentences per 100 words
S = scount / wcount * 100

index = (0.0588 * L) - (0.296 * S) - 15.8
rndindex = round(index)

if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade: " + str(rndindex))
