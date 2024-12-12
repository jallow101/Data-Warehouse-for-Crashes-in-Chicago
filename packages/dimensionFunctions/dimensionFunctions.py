import sys
from datetime import datetime

sys.path.append("../packages/main/")  # Ensure the path is correct
from main import write_csv

'''def create_dimension(dataset, dimension_name, dimension_columns):
    # Extract only the necessary columns for the new CSV
    split_data = []
    seen = set()
    unique_data = []

    for row in dataset:
           #get the key of the first element in the dictionary
        #print("Creating dimension for: ", dimensions_to_create[0])
        if  dimension_name != "Damage_to_User":
                print("Creating dimension for: ", dimension_name)
                #print("Dimension columns: ", dimension_columns)
                if dimension_columns[0] in row and row[dimension_columns[0]] not in seen:
                    unique_data.append(row)
                    seen.add(row[dimension_columns[0]])
                    #print(unique_data)
                    filtered_row = {col: row[col] for col in dimension_columns if col in row}
                    split_data.append(filtered_row)
        else:
            filtered_row = {col: row[col] for col in dimension_columns if col in row}
            split_data.append(filtered_row)

    # Write the filtered data to a new CSV file
    #write_csv("./Dimensions/new dims/"+dimension_name + '.csv', split_data, dimension_columns)
    return split_data, dimension_name


def find_columns(data, columns):
    for column in columns:
        # Get the name of the file (key) and the columns to add (values)
        dimension_name = list(column.keys())[0]
        dimension_columns = list(column.values())[0]
        return create_dimension(data, dimension_name, dimension_columns)


def split_crash_data(dataset, columns):
    return find_columns(dataset, columns)
'''

# Function to create a dimension dataset
def create_dimension(dataset, dimension_name, dimension_columns):
    print(f"Creating dimension for: {dimension_name}")

    seen = set()
    split_data = []

    for row in dataset:
        # Only include rows where the first dimension column is unique

        if dimension_name != "Damage_to_User": 
            
            key = row.get(dimension_columns[0])
            if key not in seen:
                seen.add(key)
                filtered_row = {col: row[col] for col in dimension_columns if col in row}
                split_data.append(filtered_row)
        else:
            filtered_row = {col: row[col] for col in dimension_columns if col in row}
            split_data.append(filtered_row)

    return split_data, dimension_name

# Function to find and create multiple dimensions
def find_columns(data, dimensions):
    created_dimensions = []

    for column in dimensions:
        # Get dimension name and columns
        dimension_name = list(column.keys())[0]
        dimension_columns = list(column.values())[0]

        # Create dimension and store the result
        dimension, name = create_dimension(data, dimension_name, dimension_columns)
        created_dimensions.append((dimension, name))

    return created_dimensions

# Function to split crash data and return dimensions
def split_crash_data(dataset, dimensions):
    return find_columns(dataset, dimensions)


def create_date_dimension(dataset, date_column):
    # Headers for the date dimension CSV
    date_headers = ["DATE_ID", "DATE", "TIME", "YEAR", "MONTH", "DAY", "HOUR", "QUARTER", "WEEKEND"]

    # Dictionary to track unique dates and assign unique IDs
    unique_dates = {}
    new_dataset = []
    date_id_counter = 1

    for i, row in enumerate(dataset):
        try:
            # Ensure CRASH_DATE exists and is not empty
            if date_column not in row or not row[date_column].strip():
                print(f"Skipping row {i} due to missing or invalid {date_column}: {row}")
                continue

            full_datetime = row[date_column].strip()

            # Split the datetime string into date and time
            split_datetime = full_datetime.split(' ')
            if len(split_datetime) < 2:
                raise ValueError(f"Invalid datetime format: {full_datetime}")

            date_part = split_datetime[0]
            time_part = " ".join(split_datetime[1:])  # Handles AM/PM

            # Parse the date part
            try:
                date_obj = datetime.strptime(date_part, '%m/%d/%Y')
            except ValueError:
                raise ValueError(f"Invalid date format: {date_part}")

            # Parse the time part (supports AM/PM)
            try:
                time_obj = datetime.strptime(time_part.strip(), '%I:%M:%S %p').time()
                hour = time_obj.hour
            except ValueError as ve:
                raise ValueError(f"Invalid time format: {time_part} - {ve}")

            # Extract components
            year = date_obj.year
            month = date_obj.month
            week = date_obj.isocalendar()[1]
            day = date_obj.day
            quarter = (month - 1) // 3 + 1
            weekend = 1 if date_obj.weekday() in [5, 6] else 0

            # Create a unique key for this datetime
            unique_key = f"{date_part} {time_part}"

            # Assign a unique ID for this datetime
            if unique_key not in unique_dates:
                unique_dates[unique_key] = date_id_counter
                date_id_counter += 1

            # Create a new row
            new_row = {
                "DATE_ID": unique_dates[unique_key],
                "DATE": date_part,
                "TIME": time_part,
                "YEAR": year,
                "MONTH": month,
                "WEEK": week,
                "DAY": day,
                "HOUR": hour,
                "QUARTER": quarter,
                "WEEKEND": weekend,
            }
            new_dataset.append(new_row)


        except Exception as e:
            # Log detailed error information and continue
            print(f"Error processing row {i}: {e}")
            print(f"Row data: {row}")
        

        return new_dataset

    # Write the final dataset to a CSV file
    #write_csv('../../Data/dimensions/date_dimension.csv', new_dataset, date_headers)


def clean_vehicles(vehicle_dimension):
        #remove all rows with more than 1 empty column
        cleaned_data = []
        for row in vehicle_dimension:
            if len([col for col in row if not row[col].strip()]) <= 1:
                cleaned_data.append(row)
        return cleaned_data

def remove_duplicate_id(rows, column_name):
    ids = set()
    cleaned_rows = []

    for row in rows:
        id = row[column_name]
        if id not in ids:
            ids.add(id)
            cleaned_rows.append(row)
    return cleaned_rows