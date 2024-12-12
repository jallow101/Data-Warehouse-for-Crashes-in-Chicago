# Incremental ID generator
def id_generator(start=1):
    while True:
        yield start
        start += 1

# Create ID generators for each field
weather_id_gen = id_generator(1)
injuries_id_gen = id_generator(1001)
cause_id_gen = id_generator(2001)
geography_id_gen = id_generator(3001)

def create_unique_address_column(data):
    for record in data:
        street_name = record.get('STREET_NAME', '').strip().lower()
        beat = record.get('BEAT_OF_OCCURRENCE', '').strip().lower()
        direction = record.get('STREET_DIRECTION', '').strip().lower()
        street_no = record.get('STREET_NO', '').strip().lower()

        #cast beat to int
        beat = int(float(beat)) if beat else 0
        
        # Remove decimal points from street numbers
        street_no = street_no.split('.')[0] if '.' in street_no else street_no
        
        record['UNIQUE_ADDRESS'] = f"{beat}{direction}{street_no}"

        record['CRASH_ID'] = record['RD_NO']
        record['WEATHER_ID'] = next(weather_id_gen)
        record['INJURIES_ID'] = next(injuries_id_gen)
        record['CAUSE_ID'] = next(cause_id_gen)
        record['GEOGRAPHY_ID'] = next(geography_id_gen)

        record['UNIQUE_ADDRESS_BEAT'] =   record['BEAT_OF_OCCURRENCE']

        #set data types for NUM_UNITS, INJURIES_TOTAL, INJURIES_FATAL, INJURIES_INCAPACITATING, INJURIES_NON_INCAPACITATING, INJURIES_REPORTED_NOT_EVIDENT
        record['BEAT_OF_OCCURRENCE'] = int(float(record['BEAT_OF_OCCURRENCE'])) if record['BEAT_OF_OCCURRENCE'] else 0
        record['NUM_UNITS'] = int(float(record['NUM_UNITS'])) if record['NUM_UNITS'] else 0
        record['INJURIES_TOTAL'] = int(float(record['INJURIES_TOTAL'])) if record['INJURIES_TOTAL'] else 0
        record['INJURIES_FATAL'] = int(float(record['INJURIES_FATAL'])) if record['INJURIES_FATAL'] else 0
        record['INJURIES_INCAPACITATING'] = int(float(record['INJURIES_INCAPACITATING'])) if record['INJURIES_INCAPACITATING'] else 0
        record['INJURIES_NON_INCAPACITATING'] = int(float(record['INJURIES_NON_INCAPACITATING'])) if record['INJURIES_NON_INCAPACITATING'] else 0
        record['INJURIES_REPORTED_NOT_EVIDENT'] = int(float(record['INJURIES_REPORTED_NOT_EVIDENT'])) if record['INJURIES_REPORTED_NOT_EVIDENT'] else 0
        
    return data


def create_unique_address_dict(data, column_name):
    unique_address_dict = {}
    for record in data:
        try:
            lat = float(record['LATITUDE']) if record['LATITUDE'] not in {"", "0", "None"} else None
            lon = float(record['LONGITUDE']) if record['LONGITUDE'] not in {"", "0", "None"} else None
            if lat is not None and lon is not None:
                unique_address = record[column_name]
                if unique_address in unique_address_dict:
                    unique_address_dict[unique_address].append((lat, lon))
                else:
                    unique_address_dict[unique_address] = [(lat, lon)]
        except ValueError:
            continue
    print(f"Unique addresses with valid lat/lon: {len(unique_address_dict)}")  # Debugging
    return unique_address_dict


def calculate_average_lat_long(unique_address_dict):
    average_lat_lon = {}
    for unique_address, lat_lon_list in unique_address_dict.items():
        average_lat = sum([lat for lat, lon in lat_lon_list]) / len(lat_lon_list)
        average_lon = sum([lon for lat, lon in lat_lon_list]) / len(lat_lon_list)
        average_lat_lon[unique_address] = (average_lat, average_lon)
    return average_lat_lon

def fill_missing_lat_long(data, average_lat_lon, column_name):
    check_miss = 0
    for record in data: 
        record['INJURIES_TOTAL'] = int(float(record['INJURIES_TOTAL']))
        record['INJURIES_FATAL'] = int(float(record['INJURIES_FATAL']))

        record['INJURIES_INCAPACITATING'] = int(float(record['INJURIES_INCAPACITATING']))
        record['INJURIES_NON_INCAPACITATING'] = int(float(record['INJURIES_NON_INCAPACITATING']))
        record['INJURIES_REPORTED_NOT_EVIDENT'] = int(float(record['INJURIES_REPORTED_NOT_EVIDENT']))
        record['INJURIES_NO_INDICATION'] = int(float(record['INJURIES_NO_INDICATION']))
        record['INJURIES_UNKNOWN'] = int(float(record['INJURIES_UNKNOWN']))

        lat = str(record.get('LATITUDE'))
        lon = str(record.get('LONGITUDE'))
        if lat in {"", "0", "None"} or lon in {"", "0", "None"}:
            unique_address = record[column_name]
            if unique_address in average_lat_lon:
                record['LATITUDE'], record['LONGITUDE'] = average_lat_lon[unique_address]
                check_miss += 1
            else:
                print(f"No match for UNIQUE_ADDRESS: {unique_address}")  # Debugging
    print(f"Filled {check_miss} missing LATITUDE/LONGITUDE values")  # Debugging
    return data, check_miss


#fill missing values for location
def fill_missing_location(data):
    for record in data:
        location = record.get('LOCATION')
        if location in {"", "0", "None"}:
            lat = record.get('LATITUDE')
            lon = record.get('LONGITUDE')
            if lat and lon:
                record['LOCATION'] = f"POINT ({lat}  {lon})"
    return data

def fix_report_type(data):
    for record in data:
        # Check if REPORT_TYPE is missing or empty
        
        #set data types to int for inuries
        if not record.get('REPORT_TYPE'):  # Handles None or empty string
            # Impute based on CRASH_TYPE
            if record.get('CRASH_TYPE') == "INJURY AND / OR TOW DUE TO CRASH":
                record['REPORT_TYPE'] = "ON SCENE"
            elif record.get('CRASH_TYPE') == "NO INJURY / DRIVE AWAY":
                record['REPORT_TYPE'] = "NOT ON SCENE (DESK REPORT)"
    return data

def fix_most_severe_injury(data):
    for record in data:
        if not record.get('MOST_SEVERE_INJURY'):  # Handles None or empty string
                record['MOST_SEVERE_INJURY'] = "NO INDICATION OF INJURY"
    return data

def remove_unique_cols(columnList,data):
    for record in data:
        for column in columnList:
            record.pop(column) 
    return columnList
