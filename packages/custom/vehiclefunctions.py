# Vehicles-specific function with exact missing values handling
def clean_vehicle_data_exact(rows):
    # Step 1: Filter rows where UNIT_TYPE is DRIVER and VEHICLE_YEAR is <= 2024
    filtered_rows = []
    for row in rows:
        vehicle_year = row['VEHICLE_YEAR']
        if row['UNIT_TYPE'] == 'DRIVER' and (not vehicle_year or int(float(vehicle_year)) <= 2024):
            filtered_rows.append(row)
 
    # Step 2: Fill missing VEHICLE_YEAR by grouping by 'MAKE' and 'MODEL'
    vehicle_years = defaultdict(list)
    for row in filtered_rows:
        if row['VEHICLE_YEAR'] and row['VEHICLE_YEAR'] != 'UNKNOWN':
            vehicle_years[(row['MAKE'], row['MODEL'])].append(int(float(row['VEHICLE_YEAR'])))
    
    #for row in filtered_rows:
        if not row['VEHICLE_YEAR'] or row['VEHICLE_YEAR'] == 'UNKNOWN':
            make_model = (row['MAKE'], row['MODEL'])
            if make_model in vehicle_years:
                year_data = vehicle_years[make_model]
                row['VEHICLE_YEAR'] = int(mean(year_data)) if year_data else None
                #print('Data type of VEHICLE_YEAR: ', type(row['VEHICLE_YEAR']))
 
    # Step 3: Fill LIC_PLATE_STATE with 'XX' if NaN or 'UNKNOWN'
    #for row in filtered_rows:
        if not row['LIC_PLATE_STATE'] or row['LIC_PLATE_STATE'] == 'UNKNOWN':
            row['LIC_PLATE_STATE'] = 'XX'
    
   # Step 4: Remove rows with any missing values but keep VEHICLE_YEAR as int
    final_rows = []
    for row in filtered_rows:
        # Ensure VEHICLE_YEAR is cleaned and converted to int if it exists
        if row['VEHICLE_YEAR']:
            try:
                # Handle floating-point strings like '2003.0'
                row['VEHICLE_YEAR'] = int(float(row['VEHICLE_YEAR']))
            except ValueError:
                row['VEHICLE_YEAR'] = None  # Set to None if conversion fails
         # Ensure VEHICLE_ID and OCCUPANT_CNT are ints
        if row.get('VEHICLE_ID'):
            try:
                row['VEHICLE_ID'] = int(float(row['VEHICLE_ID']))
            except ValueError:
                row['VEHICLE_ID'] = None
        
        if row.get('OCCUPANT_CNT'):
            try:
                row['OCCUPANT_CNT'] = int(float(row['OCCUPANT_CNT']))
            except ValueError:
                row['OCCUPANT_CNT'] = None
        
        # Ensure completeness of rows
        #if all(value is not None and value != '' for value in row.values()):
        if row['VEHICLE_YEAR'] == "":
            row['VEHICLE_YEAR'] = 0
            
        final_rows.append(row)
 
    # Debugging: Print the type of VEHICLE_YEAR for confirmation
    if final_rows:
        print('Data type of VEHICLE_YEAR:', type(final_rows[0]['VEHICLE_YEAR']))
 
    return final_rows

def handle_vehicle_data(input_file, output_file):
    data = read_csv(input_file)
    cleaned_data = clean_vehicle_data_exact(data)
    write_csv(output_file, cleaned_data)

############################################
#              END MArco Functions         #
############################################