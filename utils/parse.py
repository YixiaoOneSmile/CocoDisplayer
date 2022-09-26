def try_int(x):
    try:
        return int(x)
    except ValueError:
        return 0
