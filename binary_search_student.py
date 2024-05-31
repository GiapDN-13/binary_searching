import pandas as pd
import unicodedata

df = pd.read_csv("data.csv")


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

condition1 = df[['LastName', 'MiddleName', 'FirstName', 'RollNumber']].notnull().all(axis=1)

condition2 = df[['RollNumber', 'Fullname']].notnull().all(axis=1)

final_condition = condition1 | condition2

df_filtered = df[final_condition]

print(df_filtered.to_string())
