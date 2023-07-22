import pdfplumber
import numpy as np

pdf_file = '2023_bg_opt_in.pdf'
with pdfplumber.open(pdf_file) as pdf:
    p0 = pdf.pages[0].crop((0.01, 0.25, 0.9, 0.9))
    table = p0.extract_table(table_settings={'vertical_strategy':'text', 'horizontal_strategy': 'lines_strict'})
    print(table)