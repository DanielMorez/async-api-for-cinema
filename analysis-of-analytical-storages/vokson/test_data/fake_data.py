import csv
from datetime import datetime


def data_generator(convert=True, batch_count=50000):
    """
    Return generator for testing data consuming
    """
    with open("test_data/test.csv") as test_csv:
        batch = []
        for line in csv.reader(test_csv):

            row =  [
                int(line[0]),
                line[1],
                line[2],
                int(line[3]),
                datetime.strptime(line[4],'%Y-%m-%d %H:%M:%S')
            ] if convert else line

            batch.append(row)

            if len(batch) >= batch_count:
                yield batch
                batch = []
        
        if len(batch) > 0:
            yield batch
