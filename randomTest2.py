id = '6dc09126-79a6-48dc-81a1-ca06d2359692'

with open('customerDatabase.txt', 'r') as file:
    all_lines = file.readlines()
    for i, j in enumerate(all_lines):
        if id in j:
            print(i)


