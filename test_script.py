import pdfplumber


with pdfplumber.open("20_deer_odds.pdf") as pdf:

    test_file = open('deer_odds.js', 'w')

    # extract text for keys
    starting_result = ''
    for page in pdf.pages:
        starting_result += page.extract_text()

    keys = []
    for line in starting_result.splitlines():
        if "Hunt":" " in line:
            keys.append(line.strip())

    i = 0
    for page in pdf.pages[1:]:
        try:
            test_file.write('{"'+keys[i]+'":'+str(page.extract_table())+'}\n')
            # print(keys[i])
            # print(page.extract_table())
            i+=1
        except Exception as err:
            print(err)

    test_file.close()
