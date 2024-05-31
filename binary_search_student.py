import pandas as pd
import unicodedata

df = pd.read_csv("data.csv")


class BinarySearchStudent():
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def add_node(self, data):
        if data == self.data:
            return

        if data < self.data:
            if self.left:
                self.left.add_node(data)
            else:
                self.left = BinarySearchStudent(data)
        else:
            if self.right:
                self.right.add_node(data)
            else:
                self.right = BinarySearchStudent(data)

    def search_node(self):
        elements = []
        if self.left:
            elements += self.left.search_node()

        elements.append(self.data)
        if self.right:
            elements += self.right.search_node()

        return elements

    def search_value(self, val):
        if self.data == val:
            return True
        elif val < self.data:
            if self.left:
                return self.left.search_value(val)
            else:
                return False
        else:
            if self.right:
                return self.right.search_value(val)
            else:
                return False


def build_tree(elements):
    root = BinarySearchStudent(elements[0])

    for numb in range(1, len(elements)):
        root.add_node(elements[numb])

    return root


def remove_accents(input_str):
    nfkd_str = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_str if not unicodedata.combining(c)])


def build_member_code(row):
    if pd.notnull(row['RollNumber']) and pd.notnull(row['Fullname']):
        fullname = row['Fullname'].strip().split()
        if len(fullname) >= 3:
            lastname = fullname[0]
            middlename = ' '.join(fullname[1:-1])
            firstname = fullname[-1]

            row['LastName'] = lastname
            row['MiddleName'] = middlename
            row['FirstName'] = firstname

            middle_initials = ''.join([word[0] for word in middlename.split()])
            member_code = f"{firstname}{lastname[0]}{middle_initials}{row['RollNumber']}"
            return remove_accents(member_code)
    return row['MemberCode']


df['MemberCode'] = df.apply(build_member_code, axis=1)

condition1 = df[['LastName', 'MiddleName', 'FirstName', 'RollNumber', 'Email']].notnull().all(axis=1)
condition2 = df[['RollNumber', 'Fullname']].notnull().all(axis=1)
final_condition = condition1 | condition2
df_filtered = df[final_condition]

df.set_index('RollNumber', inplace=True)
data_dict = df.to_dict(orient='index')

if __name__ == '__main__':
    rollnumb = [(int(numb[2::1])) for numb in data_dict]
    tree = build_tree(rollnumb)
    print(tree.search_node())
    search_input = int(input('Enter a number to search: '))
    if tree.search_value(search_input):
        print(data_dict["DE"+ str(search_input)])
    else:
        print('Not found')