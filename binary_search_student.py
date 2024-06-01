import pandas as pd
import unicodedata


class BinaryTree:
    def __init__(self, data):
        self._data = data
        self._left = None
        self._right = None

    def add_node(self, data):
        if data == self._data:
            return

        if data < self._data:
            if self._left:
                self._left.add_node(data)
            else:
                self._left = BinaryTree(data)
        else:
            if self._right:
                self._right.add_node(data)
            else:
                self._right = BinaryTree(data)

    def search_node(self):
        elements = []
        if self._left:
            elements += self._left.search_node()

        elements.append(self._data)
        if self._right:
            elements += self._right.search_node()
        return elements

    def search_value(self, val):
        path = []
        found = self._search_value_helper(val, path)
        return found, path

    def _search_value_helper(self, val, path):
        path.append(self._data)
        if self._data == val:
            return True

        elif val < self._data:
            if self._left:
                return self._left._search_value_helper(val, path)
            else:
                return False

        else:
            if self._right:
                return self._right._search_value_helper(val, path)
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
        self._df = pd.read_csv(file_path)
        self._data_dict = {}

    @staticmethod
    def _remove_accents(input_str):
        nfkd_str = unicodedata.normalize('NFKD', input_str)
        return ''.join([c for c in nfkd_str if not unicodedata.combining(c)])

    def _build_member_code(self, row):
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
                return self._remove_accents(member_code)
        return row['MemberCode']

    def process_data(self):
        self._df['MemberCode'] = self._df.apply(self._build_member_code, axis=1)

        condition1 = self._df[['LastName', 'MiddleName', 'FirstName', 'RollNumber', 'Email']].notnull().all(axis=1)
        condition2 = self._df[['RollNumber', 'Fullname']].notnull().all(axis=1)
        final_condition = condition1 | condition2
        df_filtered = self._df[final_condition]

        df_filtered.set_index('RollNumber', inplace=True)
        self._data_dict = df_filtered.to_dict(orient='index')

    def get_data_dict(self):
        return self._data_dict


if __name__ == '__main__':
    data_processor = DataProcessor("E:\\FPT University\\2024\\SUM_24\\CSD203\\Sourcode\\binary_searching\\data.csv")
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
