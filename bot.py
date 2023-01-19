import csv
import os


class Bot:
    # Save the data to the specified csv file
    def save_data_to_csv(self, path: str, data: dict):
        with open(path, 'a') as f:
            fieldnames = ['电影名', '导演', '评级']
            csvw = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\n')
            if not os.path.getsize(path):
                csvw.writeheader()
            csvw.writerows([data])
