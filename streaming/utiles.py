def round_to_even(num):
    num = int(num) if ((int(num) % 2) == 0) else int(num) + 1
    return num
