import csv
from datetime import datetime


def read_csv(file_path, header=False):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        rows = [row for row in reader]
        if header:
            return  rows,reader.fieldnames
    return rows

# Function to write CSV data
def write_csv(file_path, rows, headers=None):
    with open(file_path, 'w', newline='') as file:
        fieldnames = list(rows[1].keys())
        if headers is None:
          # If headers are not provided, infer from the first row of data
            headers = rows[0].keys() if rows else []
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    


def remove_null(data):
    # Define null-like values to filter out
    null_values = {"", "0", "None", None}

    # Process data to filter rows
    filtered_data = []
    for record in data:
        if all(value not in null_values and str(value).strip() != "" for value in record.values()):
            filtered_data.append(record)
    return filtered_data


def left_join(left_data, right_data, on_key):
    # Convert the right dataset to a dictionary for fast lookups
    right_dict = {}
    for row in right_data:
        key = row.get(on_key)
        if key is not None:
            if key not in right_dict:
                right_dict[key] = []
            right_dict[key].append(row)
    
    # Perform the left join
    merged_data = []
    for left_row in left_data:
        key_value = left_row.get(on_key)
        matching_rows = right_dict.get(key_value, [])
        
        if matching_rows:
            for right_row in matching_rows:
                merged_row = {**left_row, **right_row}
                merged_data.append(merged_row)
        else:
            merged_data.append(left_row)

    return merged_data

def my_left_join(left_data, right_data, on_key):

    left_keys = [ ]
    #get the keys of the left data
    for row in left_data:
        left_key = row.get(on_key)


def left_join1(base_data, join_data, key_column):
    join_dict = {row[key_column]: row for row in join_data}
    result = []
    for base_row in base_data:
        key = base_row[key_column]
        joined_row = base_row.copy()
        if key in join_dict:
            joined_row.update(join_dict[key])
        result.append(joined_row)
    return result


def create_date_dimension(dataset, date_column):
    # Headers for the date dimension CSV
    date_headers = ["DATE_ID", "DATE", "TIME", "YEAR", "MONTH", "WEEK", "DAY", "HOUR", "QUARTER", "WEEKEND"]

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
            day = date_obj.day
            quarter = (month - 1) // 3 + 1
            weekend = 1 if date_obj.weekday() in [5, 6] else 0
            week  = date_obj.isocalendar()[1]

            # Create a unique key for this datetime
            unique_key = f"{date_part} {time_part}"

            # Assign a unique ID for this datetime
            if unique_key not in unique_dates:
                unique_dates[unique_key] = date_id_counter
                date_id_counter += 1

            # Add the date dimension details to the current row
            row["DATE_ID"] = unique_dates[unique_key]
            row["DATE"] = date_part
            row["TIME"] = time_part
            row["YEAR"] = year
            row["MONTH"] = month
            row["WEEK"] =  week
            row["DAY"] = day
            row["HOUR"] = hour
            row["QUARTER"] = quarter
            row["WEEKEND"] = weekend

            new_dataset.append(row)  # Append the updated row to the new dataset

        except Exception as e:
            # Log detailed error information and continue
            print(f"Error processing row {i}: {e}")
            print(f"Row data: {row}")

    return dataset
