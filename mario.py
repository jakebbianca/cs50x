from cs50 import get_int

def get_height():
    h = get_int("Height: ")
    return h


def confirm_height():
    h = get_height()

    while h < 1 or h > 8:
        h = get_height()


    return h

def main(h):
    n = 1
    while n <= h:
        if n == h:
            print(f"#" * n, "", "#" * n)
        else:
            print(f" " * (h - n - 1), "#" * n, "", "#" * n)
        n += 1


h = confirm_height()

main(h)