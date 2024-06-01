import pandas as pd
import unicodedata


class BinaryTree:
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
                self.left = BinaryTree(data)
        else:
            if self.right:
                self.right.add_node(data)
            else:
                self.right = BinaryTree(data)

    def search_node(self):
        elements = []
        if self.left:
            elements += self.left.search_node()

        elements.append(self.data)
        if self.right:
            elements += self.right.search_node()

        return elements

    def search_value(self, val):
        path = []
        found = self._search_value_helper(val, path)
        return found, path

    def _search_value_helper(self, val, path):
        path.append(self.data)
        if self.data == val:
            return True
        elif val < self.data:
            if self.left:
                return self.left._search_value_helper(val, path)
            else:
                return False
        else:
            if self.right:
                return self.right._search_value_helper(val, path)
            else:
                return False


class BinarySearchStudentTree(BinaryTree):
    def __init__(self, data):
        super().__init__(data)

    @classmethod
    def build_tree(cls, elements):
        root = cls(elements[0])
        for numb in elements[1:]:
            root.add_node(numb)
        return root


class DataProcessor:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.data_dict = {}

    @staticmethod
    def remove_accents(input_str):
        nfkd_str = unicodedata.normalize('NFKD', input_str)
        return ''.join([c for c in nfkd_str if not unicodedata.combining(c)])

    def build_member_code(self, row):
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
                return DataProcessor.remove_accents(member_code)
        return row['MemberCode']

    def process_data(self):
        self.df['MemberCode'] = self.df.apply(self.build_member_code, axis=1)

        condition1 = self.df[['LastName', 'MiddleName', 'FirstName', 'RollNumber', 'Email']].notnull().all(axis=1)
        condition2 = self.df[['RollNumber', 'Fullname']].notnull().all(axis=1)
        final_condition = condition1 | condition2
        df_filtered = self.df[final_condition]

        df_filtered.set_index('RollNumber', inplace=True)
        self.data_dict = df_filtered.to_dict(orient='index')

    def get_data_dict(self):
        return self.data_dict


if __name__ == '__main__':
    data_processor = DataProcessor("data.csv")
    data_processor.process_data()
    data_dict = data_processor.get_data_dict()

    rollnumb = [int(numb[2:]) for numb in data_dict]
    tree = BinarySearchStudentTree.build_tree(rollnumb)
    print(tree.search_node())

    search_input = int(input('Enter a number to search: '))
    found, path = tree.search_value(search_input)
    if found:
        print("search ways:", " -> ".join(map(str, path)))
        print("student data:", data_dict["DE" + str(search_input)])
    else:
        print("search ways:", " -> ".join(map(str, path)))
        print('Not found')
