import pdfplumber
import re
import csv

pdf_file = "2022_biggameapp.pdf"
csv_file = "file_for_daddy.csv"
tables=[]
with pdfplumber.open(pdf_file) as pdf:

    test_file = open(csv_file, 'w')
    problem_lines = open("problem_lines.csv", 'w')
    pages = pdf.pages
    for i,pg in enumerate(pages):
        tbl = pages[i].extract_table()
        if tbl is not None:
            if len(tbl) > 0:
                for row in tbl:
                    for cell in row:
                        result = re.match('(.*) ([0-9] - Successful)(.*)( [A-Z][A-Z] ) (.*) - (.*)\\n(.*)', cell)
                        if result is not None:
                            test_file.write(f'{result.group(1)}, {result.group(2)}, {result.group(3)}, {result.group(4)}, {result.group(5)}, {result.group(6)}, {result.group(7)}, \n')
                        else:  # try different regex
                            result = re.match('(.*)( [0-9] - Successful )(.*)( [A-Z][A-Z] )([0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9])(.*)-(.*)', cell)
                            if result is not None:
                                test_file.write(f'{result.group(1)}, {result.group(2)}, {result.group(3)}, {result.group(4)}, {result.group(5)}, {result.group(6)}, {result.group(7)}, \n')
                            else:
                                problem_lines.write(cell + '\n')