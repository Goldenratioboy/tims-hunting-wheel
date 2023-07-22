import pdfplumber
import re
import numpy as np
import tabula


# worked for 23_bg-odds
pdf_file = "23_bg-odds.pdf"

# Helper method that takes a numpy array. Returns the lowest point value with '1 in 1.0' odds
def get_lowest_points(arr):
    curr_points = 100
    for line in arr:
        if '1 in 1.0' in line and line[0] != 'Totals':
            test_val = int(line[0])
            if curr_points > test_val:
                curr_points = test_val
    if curr_points == 100:
        return 'null'
    return curr_points

# Helper method to take string such as '1 in 3' and convert it to float
def get_success_ratio(input):
    if input == 'N/A':
        return 'null'
    if input[0] != '1':
        input = '1 ' + input
    my_re = re.match(r'([0-9]) in ([0-9]+.[0-9]+)', input)
    number_one = float(my_re.group(1))
    number_two = float(my_re.group(2))
    return round(number_one / number_two, 2)

with pdfplumber.open(pdf_file) as pdf:

    for i, pg in enumerate(pdf.pages):

        try:
            pg = pdf.pages[i]
            # This section gets hunt_id, species, and weapon_type
            curr_page = pg.extract_text().splitlines()
            hunting_info = curr_page[1]
            my_match = re.match(r'Hunt: ([A-Z]{2}[0-9]{4}) (.+) - (.+) Page .+', hunting_info)
            hunt_id = my_match.group(1).strip()
            species = my_match.group(2).strip()
            weapon = my_match.group(3).strip()

            # this section gets excel screenshot information for resident & non-resident
            test_page = pg.extract_table()
            page_2d_array = []
            for x in test_page:
                row = []
                for y in x:
                    if y != None and y != '':
                        row.append(y)
                page_2d_array.append(row)

            arr = np.array(page_2d_array)

            # resident/non-resident data is in the same table, slice by columns to get two seperate tables
            resident_data = arr[:, 0:6]
            non_resident_data = arr[:, 6:]
            resident_points_gtd = get_lowest_points(resident_data)
            non_resident_points_gtd = get_lowest_points(non_resident_data)
            resident_permit_numbers = resident_data[-1, 4]
            non_resident_permit_numbers = non_resident_data[-1, 4]
            resident_odds = get_success_ratio(resident_data[-1, -1])
            non_resident_odds = get_success_ratio(non_resident_data[-1, -1])

            # final output
            # print(f"('{hunt_id}', '{species}', '{weapon}', {resident_points_gtd}, {resident_permit_numbers}, {resident_odds}, {non_resident_points_gtd}, {non_resident_permit_numbers}, {non_resident_odds}),")

            # print directly to csv-friendly format
            # need to put "" around fields w/ commas
            print(f"{hunt_id}, \"{species}\", {weapon}, {resident_points_gtd}, {resident_permit_numbers}, {resident_odds}, {non_resident_points_gtd}, {non_resident_permit_numbers}, {non_resident_odds},")

        except Exception as err:
            pass  # errors are now for the weird pages in between
            # print(err, i)
