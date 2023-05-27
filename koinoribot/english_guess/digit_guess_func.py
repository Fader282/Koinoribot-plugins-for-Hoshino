import random


def get_random_int(length):
    value = random.randint(10 ** (length - 1), 10 ** length - 1)
    return value