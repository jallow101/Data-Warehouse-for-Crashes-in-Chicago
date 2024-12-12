import csv
from collections import Counter, defaultdict
from statistics import median, mode, mean
from datetime import datetime


# Function to read CSV files
def hi(msg):
    print(msg)

def calculate_median_mode_values(rows):
    age_data = defaultdict(list)
    damage_data = defaultdict(lambda: defaultdict(list))
    sex_counter = defaultdict(Counter)
    column_data = defaultdict(lambda: defaultdict(list))

    for row in rows:
        person_type = row['PERSON_TYPE']
        
        # Collect AGE data
        if row['AGE'] not in ['UNKNOWN', 'N/A', '', None]:
            try:
                age_data[person_type].append(float(row['AGE']))
            except ValueError:
                pass

        # Collect DAMAGE data
        damage = row['DAMAGE']
        damage_category = row.get('DAMAGE_CATEGORY', 'UNKNOWN')
        if damage not in ['UNKNOWN', '', None]:
            try:
                damage_data[person_type][damage_category].append(float(row['DAMAGE']))
            except ValueError:
                pass

        # Collect SEX data
        if row['SEX'] not in ['UNKNOWN', 'N/A', '', None]:
            sex_counter[person_type].update([row['SEX']])

        # Collect other column data
        for col, value in row.items():
            if col not in ['PERSON_TYPE', 'AGE', 'DAMAGE', 'SEX'] and value not in ['UNKNOWN', 'N/A', '', None]:
                column_data[person_type][col].append(value)

    medians = {
        'age': {ptype: median(values) for ptype, values in age_data.items() if values},
        'damage': {
            ptype: {
                category: median(damage_list) for category, damage_list in categories.items() if damage_list
            } for ptype, categories in damage_data.items()
        },
    }
    modes = {
        'sex': {ptype: sex_counter[ptype].most_common(1)[0][0] for ptype in sex_counter},
        'other_columns': {
            ptype: {col: mode(values) for col, values in cols.items() if values}
            for ptype, cols in column_data.items()
        },
    }

    return medians, modes


def assign_vehicle_id(row):
            
    if row['PERSON_TYPE'] == 'DRIVER':
        return int(0)
    elif row['PERSON_TYPE'] == 'PASSENGER':
        return int(1)
    elif row['PERSON_TYPE'] == 'PEDESTRIAN':
        return int(2)
    elif row['PERSON_TYPE'] == 'BICYCLE':
        return int(3)
    elif row['PERSON_TYPE'] == 'MOTORCYCLE':
        return int(4)
    else:
        return int(5)

# Function to clean and fill people dataset
def fill_and_clean_people_data(rows, medians, modes):
    cleaned_rows = []
    for row in rows:
        person_type = row['PERSON_TYPE']
        damage_category = row.get('DAMAGE_CATEGORY', 'UNKNOWN')


        row['AGE'] = medians['age'].get(person_type, 'NOT APPLICABLE') if row['AGE'] in ['UNKNOWN', 'N/A', '', None] else row['AGE']
        row['AGE'] = int(float(row['AGE']))
        if row['VEHICLE_ID'] not in ['UNKNOWN', 'N/A', '', None]:
            try:
                row['VEHICLE_ID'] = int(float(row['VEHICLE_ID']))
            except ValueError:
                row['VEHICLE_ID'] = None
            #row['VEHICLE_ID'] = int(float(row['VEHICLE_ID']))
        #else:
            #row['VEHICLE_ID'] = None
        
        
        if row['DAMAGE'] in ['UNKNOWN', 'N/A', '', None]:
            if damage_category == '$500 OR LESS':
                row['DAMAGE'] = 250.0
            else:
                damage_value = medians['damage'].get(person_type, {}).get(damage_category, 'UNKNOWN')
                row['DAMAGE'] = round(damage_value, 2)        
        
        row['SEX'] = modes['sex'].get(person_type, 'NOT APPLICABLE') if row['SEX'] in ['UNKNOWN', 'N/A', '', None] else row['SEX']

        if not row['VEHICLE_ID'] or  row['VEHICLE_ID'] == "":
                if row['PERSON_TYPE'] == 'BICYCLE':
                    row['VEHICLE_ID'] = 900000
                elif row['PERSON_TYPE'] == 'PEDESTRIAN':
                    row['VEHICLE_ID'] = 900001
                elif row['PERSON_TYPE'] == 'NON-MOTOR VEHICLE':
                    row['VEHICLE_ID'] = 900002
                elif row['PERSON_TYPE'] == 'NON-CONTACT VEHICLE':
                    row['VEHICLE_ID'] = 900003
                elif row['PERSON_TYPE'] == 'PASSESNGER':
                    row['VEHICLE_ID'] = 900004
                else:
                    row['VEHICLE_ID'] = 900005
        
        for col in row:
            if col not in ['PERSON_TYPE', 'AGE', 'DAMAGE', 'SEX', 'CITY', 'STATE'] and row[col] in ['UNKNOWN', 'N/A', '', None]:
                row[col] = modes['other_columns'].get(person_type, {}).get(col, 'NOT APPLICABLE')
        row['CITY'] = row.get('CITY', 'UNKNOWN') or 'UNKNOWN'
        row['STATE'] = row.get('STATE', 'Unknown') or 'XX'

        row['VEHICLE_ID'] = int(float(row['VEHICLE_ID'])) if row['VEHICLE_ID'] else 0

        cleaned_rows.append(row)
    return cleaned_rows

def create_age_group(rows):

    def getAgeGroup(age): 
        if age < 19:
            return "Younging"
        elif age > 18 and age < 25:
            return  "Youth"
        elif  age > 24 and age <36 :
            return "Adult"
        elif age > 35 and age <60 :
            return "Grown Adult"
        else:
            return "Very Old"

    #add AGR_GROUP to columns
    for row in rows:
        if row['AGE'] !="" :
            age = int(float(row['AGE']))
            row['AGE_GROUP'] = getAgeGroup(age)
           
    return rows

def remove_duplicate_person_id(rows):
    person_ids = set()
    cleaned_rows = []

    for row in rows:
        person_id = row['PERSON_ID']
        if person_id not in person_ids:
            person_ids.add(person_id)
            cleaned_rows.append(row)
    return cleaned_rows

