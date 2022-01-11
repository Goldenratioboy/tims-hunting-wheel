import re
import csv

f = open("raw_data.txt", "r")

with open('processed_data.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    for x in f:
        try:
            p_line = re.match(r'(.+)(DB|EB|PB|MB|BI|DS|RS|GO)([0-9]{4})(.+)', x)
            csvwriter.writerow([p_line.group(1), p_line.group(2)+p_line.group(3), p_line.group(4)])
        except:
            pass  # ignore the problem lines

f.close()