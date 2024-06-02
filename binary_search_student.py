import pandas as pd
import unicodedata
import json
import re


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

    def delete_node(self, data):
        if data < self._data:
            if self._left:
                self._left = self._left.delete_node(data)
        elif data > self._data:
            if self._right:
                self._right = self._right.delete_node(data)
        else:
            if self._left is None:
                return self._right
            if self._right is None:
                return self._left

            min_larger_node = self._right
            while min_larger_node._left:
                min_larger_node = min_larger_node._left
            self._data = min_larger_node._data
            self._right = self._right.delete_node(self._data)
        return self

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
        self._file_path = file_path
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

    def save_to_csv(self):
        self._df.to_csv(self._file_path, index=False)

    def add_new_student(self, roll_number, member_code, last_name, middle_name, first_name, fullname, email):
        new_student = {
            'RollNumber': roll_number,
            'MemberCode': member_code,
            'LastName': last_name,
            'MiddleName': middle_name,
            'FirstName': first_name,
            'Fullname': fullname,
            'Email': email
        }
        self._df = self._df._append(new_student, ignore_index=True)
        self.process_data()
        self.save_to_csv()

    def update_student(self, roll_number, member_code, last_name, middle_name, first_name, fullname, email):
        if roll_number in self._df['RollNumber'].values:
            self._df.loc[
                self._df['RollNumber'] == roll_number, ['MemberCode', 'LastName', 'MiddleName', 'FirstName', 'Fullname',
                                                        'Email']] = [member_code, last_name, middle_name, first_name,
                                                                     fullname, email]
            self.process_data()
            self.save_to_csv()
        else:
            print(f"Roll Number {roll_number} not found.")

    def delete_student(self, roll_number):
        if roll_number in self._df['RollNumber'].values:
            self._df = self._df[self._df['RollNumber'] != roll_number]
            self.process_data()
            self.save_to_csv()
        else:
            print(f"Roll Number {roll_number} not found.")


def validate_roll_number(roll_number):
    pattern = r'^DE\d{2}\d{4}$'
    if re.match(pattern, roll_number):
        return True
    return False


def main():
    data_processor = DataProcessor("data.csv")
    data_processor.process_data()
    data_dict = data_processor.get_data_dict()

    rollnumb = [int(numb[2:]) for numb in data_dict]
    print(f"{rollnumb}", end=" ")
    tree = BinarySearchStudentTree.build_tree(rollnumb)

    while True:
        get_input = int(input(
            "\nSelect your choice to do:\n 1. Add new data\n 2. Search data\n 3. Update data\n 4. Delete data\n 5. Exit\nEnter choice: "))
        if get_input == 1:
            roll_number = input('Enter Roll Number (follows structure: DE + school year + serial | Ex: DE180345 ): ')
            while not validate_roll_number(roll_number):
                print("Invalid Roll Number format. Please try again.")
                roll_number = input(
                    'Enter Roll Number (follows structure: DE + school year + serial | Ex: DE180345 ): ')
            last_name = input('Enter Last Name: ')
            middle_name = input('Enter Middle Name: ')
            first_name = input('Enter First Name: ')
            fullname = f"{last_name} {middle_name} {first_name}"
            member_code = DataProcessor._remove_accents(f"{first_name}{last_name[0]}{middle_name}{roll_number}")
            email = input('Enter Email: ')
            data_processor.add_new_student(roll_number, member_code, last_name, middle_name, first_name, fullname,
                                           email)
            tree.add_node(int(roll_number[2:]))
            print(f"Added student with Roll Number {roll_number} to the tree.")
        elif get_input == 2:
            search_input = int(input('\nEnter a number to search: '))
            found, path = tree.search_value(search_input)

            if found:
                print("search ways:", " -> ".join(map(str, path)))
                json_convert = json.dumps(data_dict["DE" + str(search_input)], indent=4, ensure_ascii=False)
                print(f"student data: \n {json_convert}")
            else:
                print("search ways:", " -> ".join(map(str, path)))
                print('Not found')

        elif get_input == 3:
            roll_number = input(
                'Enter Roll Number to update (follows structure: DE + school year + serial | Ex: DE180345 ): ')
            while not validate_roll_number(roll_number):
                print("Invalid Roll Number format. Please try again.")
                roll_number = input(
                    'Enter Roll Number to update (follows structure: DE + school year + serial | Ex: DE180345 ): ')
            last_name = input('Enter new Last Name: ')
            middle_name = input('Enter new Middle Name: ')
            first_name = input('Enter new First Name: ')
            fullname = f"{last_name} {middle_name} {first_name}"
            member_code = DataProcessor._remove_accents((f"{first_name}{last_name[0]}{middle_name}{roll_number}"))
            email = input('Enter new Email: ')
            data_processor.update_student(roll_number, member_code, last_name, middle_name, first_name, fullname, email)
            print(f"Updated student with Roll Number {roll_number}.")
        elif get_input == 4:
            roll_number = input(
                'Enter Roll Number to delete (follows structure: DE + school year + serial | Ex: DE180345 ): ')
            while not validate_roll_number(roll_number):
                print("Invalid Roll Number format. Please try again.")
                roll_number = input(
                    'Enter Roll Number to delete (follows structure: DE + school year + serial | Ex: DE180345 ): ')
            data_processor.delete_student(roll_number)
            tree.delete_node(int(roll_number[2:]))
            print(f"Deleted student with Roll Number {roll_number} from the tree and data.")
        elif get_input == 5:
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please select again.")


if __name__ == '__main__':
    main()
