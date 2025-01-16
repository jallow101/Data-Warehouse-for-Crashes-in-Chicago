import pyodbc
import csv
import os
from dotenv import load_dotenv
load_dotenv()
# bulk discount-  STITOY7US

# Define the connection parameters
#read dorm env file

server = 'tcp:lds.di.unipi.it' 
database = 'Group_ID_16_DB' 
username = 'Group_ID_156_CGCTCCG'
password = 'XRDTDD6CTXXXXXX' 

# Database connection string
DATABASE_CONNECTION_STRING = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};DATABASE={database};UID={username};PWD={password}'
)

# Dimensions and their columns
#Done  ---->  Vehicle, Injuries, Geography, Weather, Cause, Date,
# Failed ---->   Person, Damage_to_User, Crash
dimensions = {
    #"Injuries": ["INJURIES_ID","INJURY_CLASSIFICATION", "MOST_SEVERE_INJURY", "INJURIES_TOTAL", "INJURIES_FATAL", "INJURIES_INCAPACITATING", "INJURIES_NON_INCAPACITATING", "INJURIES_REPORTED_NOT_EVIDENT", "INJURIES_NO_INDICATION", "INJURIES_UNKNOWN"],
    #"Crash": ["CRASH_ID","FIRST_CRASH_TYPE", "REPORT_TYPE", "CRASH_TYPE"],
    #"Person": ["PERSON_ID","PERSON_TYPE", "CITY", "STATE", "SEX", "AGE","AGE_GROUP", "PHYSICAL_CONDITION", "SAFETY_EQUIPMENT", "AIRBAG_DEPLOYED", "EJECTION"],
    #"Vehicle": ["VEHICLE_ID", "UNIT_TYPE", "MAKE", "MODEL", "LIC_PLATE_STATE", "VEHICLE_YEAR", "VEHICLE_DEFECT", "VEHICLE_TYPE", "VEHICLE_USE", "TRAVEL_DIRECTION", "MANEUVER", "OCCUPANT_CNT", "FIRST_CONTACT_POINT"],
    #"Weather": ["WEATHER_ID","WEATHER_CONDITION", "LIGHTING_CONDITION"],
    #"Cause": ["CAUSE_ID","BAC_RESULT", "DRIVER_ACTION", "DRIVER_VISION", "PRIM_CONTRIBUTORY_CAUSE", "SEC_CONTRIBUTORY_CAUSE"],
    #"Geography": ["GEOGRAPHY_ID","POSTED_SPEED_LIMIT", "TRAFFIC_CONTROL_DEVICE", "DEVICE_CONDITION", "TRAFFICWAY_TYPE", "ALIGNMENT", "ROADWAY_SURFACE_COND", "ROAD_DEFECT", "STREET_NAME", "STREET_NO", "STREET_DIRECTION","BEAT_OF_OCCURRENCE", "LATITUDE", "LONGITUDE", "LOCATION"],
    "Damage_to_User": ["DATE_ID","CRASH_ID","VEHICLE_ID","INJURIES_ID","PERSON_ID","WEATHER_ID","CAUSE_ID", "GEOGRAPHY_ID","DAMAGE", "DAMAGE_CATEGORY", "NUM_UNITS","UNIT_NO"],
    #"Date": ["DATE_ID", "DATE","DATE_POLICE_NOTIFIED", "TIME", "YEAR", "MONTH","WEEK", "DAY", "HOUR", "QUARTER", "WEEKEND"]
}

# Establish a database connection
def connect_to_db():
    return pyodbc.connect(DATABASE_CONNECTION_STRING)

# Create progress tracking table
def create_progress_table():
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        # Check if the table exists and create it if not
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'ImportProgress') AND type = N'U')
            BEGIN
                CREATE TABLE ImportProgress (
                    table_name NVARCHAR(255) NOT NULL PRIMARY KEY,
                    last_row INT NOT NULL
                )
            END
        """)
        connection.commit()
        print("Progress tracking table 'ImportProgress' is ready.")
    except pyodbc.Error as e:
        print(f"Error creating progress tracking table:e")
    finally:
        connection.close()

# Get last processed row for a table
def get_last_processed_row(table_name):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT last_row FROM ImportProgress WHERE table_name = ?", (table_name,))
        result = cursor.fetchone()
        return result[0] if result else 0
    finally:
        connection.close()

# Update the last processed row for a table
def update_last_processed_row(table_name, last_row):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            MERGE ImportProgress AS target
            USING (SELECT ? AS table_name, ? AS last_row) AS source
            ON target.table_name = source.table_name
            WHEN MATCHED THEN
                UPDATE SET last_row = source.last_row
            WHEN NOT MATCHED THEN
                INSERT (table_name, last_row) VALUES (source.table_name, source.last_row);
        """, (table_name, last_row))
        connection.commit()
    finally:
        connection.close()

# Populate tables from CSV files using batch inserts
def populate_tables1(batch_size=1000):
    connection = connect_to_db()
    cursor = connection.cursor()

    directory_path = r"C:\Users\PC2\Desktop\DSS\DSS_Crashlytics_Data_Warehouse\Data\dimensions"

   # Print files in directory
    print("Files in directory:")
    for file_name in os.listdir(directory_path):
        print(file_name)

    # Verify CSV files match dimensions
    for table_name in dimensions:
        csv_file = os.path.join(directory_path, f"{table_name}.csv")
        if os.path.exists(csv_file):
            print(f"File found for table '{table_name}': {csv_file}")
        else:
            print(f"File not found for table '{table_name}'")

    for table_name, columns in dimensions.items():
        print(f"Starting import for table '{table_name}'...")
        #print(f"Columns: {columns}")
        csv_file = f"{table_name}.csv"
        csv_file= csv_file.strip()
        print(f"Starting '{csv_file}' import for table '{table_name}'...")

        last_row = get_last_processed_row(table_name)
        current_row = 0

        try:
            with open(csv_file, mode="r", encoding="utf-8") as file:
                csv_reader = csv.reader(file)

                print(csv_reader, "CSV Reader")
                headers = next(csv_reader)  # Skip the header row

                #if headers != columns:
                #    print(f"Header mismatch for '{table_name}'. Skipping.")
                #    continue

                rows = []
                for row in csv_reader:
                    current_row += 1
                    if current_row <= last_row:
                        continue  # Skip already processed rows

                    rows.append(row)
                    if len(rows) == batch_size:
                        insert_batch(cursor, table_name, columns, rows)
                        rows = []
                        update_last_processed_row(table_name, current_row)
                        print(f"Inserted up to {current_row} for table '{table_name}'.")

                if rows:
                    insert_batch(cursor, table_name, columns, rows)
                    update_last_processed_row(table_name, current_row)
                    print(f"Inserted remaining rows up to row {current_row} for table '{table_name}'.")

            print(f"Import completed for table '{table_name}'.")
        
        except FileNotFoundError:
            print(f"CSV file for '{table_name}' not found. Skipping.")
        except pyodbc.Error as e:
            print(f"Error inserting data into '{table_name}': {e}")
        finally:
            connection.commit()

    connection.close()

# Read and process CSV files
# Populate tables from CSV files using batch inserts
def populate_tables(directory_path, batch_size=1000):
    connection = connect_to_db()
    cursor = connection.cursor()

    # List all files in the directory
    files = [f for f in os.listdir(directory_path) if f.endswith(".csv")]
    print(f"Found files: {files}")

    for file_name in files:
        table_name = os.path.splitext(file_name)[0]  # Get table name without extension
        if table_name not in dimensions:
            print(f"Skipping unknown file: {file_name}")
            continue  # Skip files not listed in dimensions

        columns = dimensions[table_name]
        csv_file = os.path.join(directory_path, file_name)

        print(f"Processing file '{csv_file}' for table '{table_name}' with columns: {columns}")

        try:
            # Count the total rows for progress tracking
            with open(csv_file, mode="r", encoding="utf-8") as file:
                total_rows = sum(1 for _ in file) - 1  # Subtract 1 for the header row

            with open(csv_file, mode="r", encoding="utf-8") as file:
                csv_reader = csv.reader(file)
                headers = next(csv_reader)  # Skip the header row

                # Validate headers
                if headers != columns:
                    print(f"Header mismatch for '{table_name}'. Expected: {columns}, Found: {headers}. Skipping.")
                    continue

                rows = []
                inserted_count = 0
                for i, row in enumerate(csv_reader, start=1):
                    rows.append(row)
                    if len(rows) == batch_size:  # Insert in batches
                        insert_batch(cursor, table_name, columns, rows)
                        inserted_count += len(rows)
                        rows = []  # Clear the batch

                        # Display progress
                        progress = (inserted_count / total_rows) * 100
                        print(f"Progress for '{table_name}': {progress:.2f}% ({inserted_count}/{total_rows} rows)")

                # Insert remaining rows
                if rows:
                    insert_batch(cursor, table_name, columns, rows)
                    inserted_count += len(rows)
                    progress = (inserted_count / total_rows) * 100
                    print(f"Progress for '{table_name}': {progress:.2f}% ({inserted_count}/{total_rows} rows)")

                print(f"Completed processing for table '{table_name}'. Total rows inserted: {inserted_count}")

        except FileNotFoundError:
            print(f"File not found: {csv_file}")
        except Exception as e:
            print(f"Error processing file '{csv_file}': {e}")

    connection.commit()
    connection.close()


# Function to insert a batch of rows
def insert_batch(cursor, table_name, columns, rows):
    placeholders = ", ".join(["?" for _ in columns])  # Create placeholders for parameterized query
    insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
    try:
        cursor.executemany(insert_sql, rows)  # Execute batch insert
    except pyodbc.Error as e:
        print(f"Error during batch insert into '{table_name}': {e}")

# Main function to execute the script
if __name__ == "__main__":

    #directory_path = r"C:\Users\PC2\Desktop\DSS\Project\Scripts\Dimensions\new dims"
    print("Creating progress tracking table...")
    #create_progress_table()
    print("Populating tables...")
    directory_path = r"C:\Users\PC2\Desktop\DSS\DSS_Crashlytics_Data_Warehouse\Data\dimensions"
    populate_tables(directory_path ,batch_size=4000)  # Adjust batch size for performance
    print("Done.")
