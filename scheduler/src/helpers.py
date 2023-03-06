def create_chunks(list_name, step):
    for i in range(0, len(list_name), step):
        yield list_name[i: i + step]
